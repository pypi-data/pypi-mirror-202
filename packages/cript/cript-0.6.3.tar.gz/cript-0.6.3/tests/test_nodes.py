import json
from tempfile import NamedTemporaryFile
from unittest import mock

import psycopg2
import pytest
import requests
from requests.exceptions import ConnectionError

import cript

MY_GROUP = "MyGroup"
MY_PROJECT = "MyProject"
MY_COLLECTION = "Test"
MY_EXPERIMENT = "Anionic Polymerization of Styrene with SecBuLi"
MY_INVENTORY = "Test"
MY_PROCESS = "Test"


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("web", 8000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=6000.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def db_connection(docker_ip, docker_services):
    port = docker_services.port_for("db", 5432)
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host=docker_ip,
        port=port,
    )
    return conn


@pytest.fixture(scope="session")
def web_token(docker_ip, docker_services, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                t.key
            FROM authtoken_token t
            JOIN accounts_user a ON a.id=t.user_id
            WHERE a.email='test@test.com'
        """
        )

        data = cursor.fetchone()
        return data[0]


@pytest.fixture(scope="session")
def criptapp_api(http_service, web_token):
    return cript.API(http_service, f"Token {web_token}", tls=False)


def test_status_code(http_service):
    status = 200
    response = requests.get(http_service + "/")

    assert response.status_code == status


@pytest.mark.filterwarnings("error::UserWarning")
def test_create_group_success(criptapp_api):
    group = cript.Group(name=MY_GROUP)
    group.save()


def test_create_project_success(criptapp_api):
    project = cript.Project(name=MY_PROJECT)
    project.save()


def test_create_collection_success(criptapp_api):
    proj = cript.Project.get(name=MY_PROJECT)
    coll = cript.Collection(project=proj, name=MY_COLLECTION)
    coll.save()


def test_create_experiment_success(criptapp_api):
    coll = cript.Collection.get(name=MY_COLLECTION)
    expt = cript.Experiment(collection=coll, name=MY_EXPERIMENT)
    expt.save()


def test_create_process_success(criptapp_api):
    expt = cript.Experiment.get(name=MY_EXPERIMENT)

    process = cript.Process(
        experiment=expt,
        name=MY_PROCESS,
        type="multistep",
        description="In an argon filled glovebox, a round bottom flask was filled with 216 ml of dried toluene. The "
        "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
        "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
        "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
        "precipitation in methanol 3 times and dried under vacuum.",
    )
    process.save()


def test_create_material(criptapp_api):
    proj = cript.Project.get(name=MY_PROJECT)
    cript.Material.create(project=proj, name="SecBuLi solution 1.4M cHex")
    cript.Material.create(project=proj, name="toluene")
    cript.Material.create(project=proj, name="styrene")
    cript.Material.create(project=proj, name="1-butanol")
    cript.Material.create(project=proj, name="methanol")


def test_create_inventory(criptapp_api):
    coll = cript.Collection.get(name=MY_COLLECTION)
    solution = cript.Material.get(name="SecBuLi solution 1.4M cHex")
    toluene = cript.Material.get(name="toluene")
    styrene = cript.Material.get(name="styrene")
    butanol = cript.Material.get(name="1-butanol")
    methanol = cript.Material.get(name="methanol")
    inv = cript.Inventory(
        collection=coll,
        name=MY_INVENTORY,
        materials=[solution, toluene, styrene, butanol, methanol],
    )
    inv.save()


def test_get_material(criptapp_api, http_service, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT uid from core_inventory WHERE name='{MY_INVENTORY}'
        """
        )
        inventory_uid = cursor.fetchone()[0]
        inv = cript.Inventory.get(uid=inventory_uid)
        assert type(inv.materials[0]) is cript.data_model.nodes.material.Material


def test_add_ingredient_to_process_node(criptapp_api, http_service, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT uid from core_inventory WHERE name='{MY_INVENTORY}'
        """
        )
        inventory_uid = cursor.fetchone()[0]
        url = f"{http_service}/inventory/{inventory_uid}/"
        inv = cript.Inventory.get(url=url, get_level=1)

    prcs = cript.Process.get(name=MY_PROCESS)
    solution = inv["SecBuLi solution 1.4M cHex"]
    toluene = inv["toluene"]
    styrene = inv["styrene"]
    butanol = inv["1-butanol"]
    methanol = inv["methanol"]

    # define Quantity nodes indicating the amount of each Ingredient.
    initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
    solvent_qty = cript.Quantity(key="volume", value=10, unit="ml")
    monomer_qty = cript.Quantity(key="mass", value=0.455, unit="g")
    quench_qty = cript.Quantity(key="volume", value=5, unit="ml")
    workup_qty = cript.Quantity(key="volume", value=100, unit="ml")

    # create Ingredient nodes for each.
    initiator = cript.Ingredient(
        keyword="initiator", material=solution, quantities=[initiator_qty]
    )
    solvent = cript.Ingredient(
        keyword="solvent", material=toluene, quantities=[solvent_qty]
    )
    monomer = cript.Ingredient(
        keyword="monomer", material=styrene, quantities=[monomer_qty]
    )
    quench = cript.Ingredient(
        keyword="quench", material=butanol, quantities=[quench_qty]
    )
    workup = cript.Ingredient(
        keyword="workup", material=methanol, quantities=[workup_qty]
    )

    prcs.add_ingredient(initiator)
    prcs.add_ingredient(solvent)
    prcs.add_ingredient(monomer)
    prcs.add_ingredient(quench)
    prcs.add_ingredient(workup)

    # add the Ingredient nodes to the Process node.
    prcs.add_ingredient(initiator)
    prcs.add_ingredient(solvent)
    prcs.add_ingredient(monomer)
    prcs.add_ingredient(quench)
    prcs.add_ingredient(workup)


def test_add_condition_nodes_to_process_nodes(criptapp_api):
    prcs = cript.Process.get(name=MY_PROCESS)
    temp = cript.Condition(key="temperature", value=25, unit="celsius")
    time = cript.Condition(key="time_duration", value=60, unit="min")
    prcs.add_condition(temp)
    prcs.add_condition(time)


def test_add_property_node_to_process_node(criptapp_api):
    prcs = cript.Process.get(name=MY_PROCESS)
    yield_mass = cript.Property(key="yield_mass", value=0.47, unit="g", method="scale")
    prcs.add_property(yield_mass)


def test_create_material_process_product(criptapp_api):
    proj = cript.Project.get(name=MY_PROJECT)
    prcs = cript.Process.get(name=MY_PROCESS)
    polystyrene = cript.Material(project=proj, name="polystyrene")

    names = cript.Identifier(key="names", value=["poly(styrene)", "poly(vinylbenzene)"])
    bigsmiles = cript.Identifier(
        key="bigsmiles", value="[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"
    )
    chem_repeat = cript.Identifier(key="chem_repeat", value="C8H8")
    cas = cript.Identifier(key="cas", value="100-42-5")

    polystyrene.add_identifier(names)
    polystyrene.add_identifier(chem_repeat)
    polystyrene.add_identifier(bigsmiles)
    polystyrene.add_identifier(cas)

    phase = cript.Property(key="phase", value="solid")
    color = cript.Property(key="color", value="white")

    polystyrene.add_property(phase)
    polystyrene.add_property(color)
    polystyrene.save()

    prcs.add_product(polystyrene)
    prcs.save()


def test_create_data_node(criptapp_api):
    expt = cript.Experiment.get(name=MY_EXPERIMENT)
    polystyrene = cript.Material.get(name="polystyrene")

    sec = cript.Data(experiment=expt, name="Crude SEC of polystyrene", type="sec_trace")
    sec.save()

    # Associate a Data node with a Property node
    mw_n = cript.Property(key="mw_n", value=5200, unit="g/mol")
    mw_n.data = sec
    polystyrene.add_property(mw_n)
    polystyrene.save()


def test_create_file_node_and_upload(criptapp_api):
    with mock.patch.object(cript.File, "save", new=lambda *args: None):
        with NamedTemporaryFile(suffix=".csv") as tmp:
            proj = cript.Project.get(name=MY_PROJECT)
            f = cript.File(project=proj, source=tmp.name)
            f.save()
