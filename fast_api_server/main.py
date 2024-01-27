from fastapi import FastAPI, Depends, HTTPException, responses, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from fast_api_server.service import Service
from typing import List

from database.database import engine, get_db
from database.models import Sources, Durations, Ranges, Spell
from database import models
from . import schemas


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
To run server pleas enter the following command 
cd directory/to/your/practice/file 
then enter
uvicorn fast_api_server.main:app --reload
beforehand you must have installed venv and all requirements
"""


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/spells")
async def dbtest(db: Session = Depends(get_db)):
    """
    Get short information of each spell in the database.

    **DO NOT INSERT ANYTHING.**

    If the response is like this "Something went wrong with the database, please contact the owner,"
    then something went wrong with your local database delete file and read documentation for database_fulfillment.

    Returns:
    - `status`: A string indicating the status of the request.
    - `data`: A list of dictionaries containing short information about each spell.

    Raises:
    - `HTTPException`: If there is an issue with the database.

    Example Usage:
    ```python
    response = client.get("/spells")
    assert response.status_code == 200
    assert response.json()["status"] == "spell"
    assert len(response.json()["data"]) > 0
    ```

    """
    service_instance = Service()
    result = (
        db.query(Spell, Durations, Ranges)
        .join(Durations, Durations.id == Spell.duration_id)
        .join(Ranges, Ranges.id == Spell.spell_range_id)
    )


    # Data consistency check
    if None in result:
        # if data is corrupted
        raise HTTPException(status_code=404, detail="Something went wrong with database pleas contact owner")
    else:
        # if data is correct then return list of dicts
        formatted_result = service_instance.format_result_for_all_spells(result.all())
        print(result.all())
        return {
            "status": "spell",
            "data": formatted_result
        }


@app.get("/get-spell/{spell_id}")
async def get_spell(spell_id: int, db: Session = Depends(get_db)):
    """
    Retrieve information about a spell by its ID.

    Parameters:
    - `spell_id`: The unique identifier for the spell.

    Returns:
    - `status`: A string indicating the status of the request.
    - `data`: A list of dictionaries containing information about the spell.

    Raises:
    - `HTTPException`: If there is an issue with the database or the requested spell is not found.

    Example Usage:
    ```JavaScript
    // Fetch spell information by ID
    async function getSpellById(spellId) {
    const response = await fetch(`http://localhost:8000/get-spell/${spellId}`);
    const data = await response.json();

    if (response.status !== 200) {
        console.error(`Error: ${data.detail}`);
        // Handle error appropriately
        return null;
    }

    console.log("Spell Data:", data.data);
    return data.data;
    }

    // Example Usage
    const spellId = 1; // Replace with the desired spell ID
    getSpellById(spellId);
    ```
    """
    service_instance = Service()

    result = (
        db.query(Spell, Sources.book_name, Durations, Ranges)
        .join(Sources, Sources.id == Spell.source_id)
        .join(Durations, Durations.id == Spell.duration_id)
        .join(Ranges, Ranges.id == Spell.spell_range_id)
        .filter(Spell.id == spell_id)
    ).all()

    # Data consistency check
    if None in result:
        # if data is corrupted
        raise HTTPException(status_code=404, detail="Something went wrong with database pleas contact owner")
    else:
        # if data is correct then return list of dicts
        formatted_result = service_instance.format_spell(result)
        return {
            "status": "pussy test",
            "data": formatted_result
        }


@app.get("/data-sort/")
async def data_filter(filter_name: str, asc_value: bool = True, db: Session = Depends(get_db)):
    """
    Endpoint to filter and retrieve data based on different criteria.

    Args:
        filter_name (str): The filter criteria (e.g., "lvl", "name", "concentration", "duration", "time", "range").
        asc_value (bool, optional): Ascending order if True, descending order if False. Default is True.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the status and filtered data.

    Raises:
        HTTPException: Raised if there is an issue with the database or if the data is corrupted.

    Notes:
        The endpoint supports filtering data based on different criteria such as spell level, spell name,
        concentration, duration, casting time, and spell range.

        - For `filter_name` = "lvl", the data is filtered and ordered by spell level.
        - For `filter_name` = "name", the data is filtered and ordered by spell name.
        - For `filter_name` = "concentration", the data is filtered based on concentration (1 for True, 0 for False).
        - For `filter_name` = "duration", the data is filtered and ordered by spell duration `to get non-durational
         spells first do not pass anithing to asc_value else pass False`
        - For `filter_name` = "time", the data is filtered and ordered by casting time.
        - For `filter_name` = "range", the data is filtered and ordered by spell range.

        The result is returned as a dictionary with a status and a list of dictionaries containing the formatted data.

    Example:
        To retrieve spells ordered by level in descending order:
        ```
        /data_filter/?filter_name=lvl&asc_value=False
        ```

        To retrieve spells with concentration in ascending order:
        ```
        /data_filter/?filter_name=concentration&asc_value=True
        ```
    """
    service_instance = Service()
    result = (
            db.query(Spell, Durations, Ranges)
            .join(Durations, Durations.id == Spell.duration_id)
            .join(Ranges, Ranges.id == Spell.spell_range_id)
        )
    if filter_name == "lvl":
        result = (
            result.order_by(asc(Spell.spell_level) if asc_value is True else desc(Spell.spell_level))
        )

    elif filter_name == "name":
        result = (
            result.order_by(asc(Spell.spell_name) if asc_value is True else desc(Spell.spell_name))
        )

    elif filter_name == "concentration":
        result = (
            result.order_by(Durations.concentration.asc() if asc_value is True else Durations.concentration.desc())
        )

    elif filter_name == "duration":
        result = (
            result.order_by(asc(Durations.duration_time) if asc_value is True else desc(Durations.duration_time))
            .order_by(desc(Durations.duration_type))
        )

    elif filter_name == "time":
        result = (
            result.order_by(asc(Spell.cast_time) if asc_value is True else desc(Spell.cast_time))
        )

    elif filter_name == "range":
        result = (
            result.order_by(asc(Ranges.distance_range) if asc_value is True else desc(Ranges.distance_range))
            .order_by(desc(Durations.duration_type))
        )

    if None in result:
        # if data is corrupted
        raise HTTPException(status_code=404, detail="Something went wrong with database pleas contact owner")
    else:
        # if data is correct then return list of dicts
        formatted_result = service_instance.format_result_for_all_spells(result.all())
        return {
            "status": "pussy test",
            "data": formatted_result
        }


@app.get("/data-filter/")
async def data_filter(
        level: int = None,
        caster_class: str = None,
        school: str = None,
        damage_type: str = None,
        range_distance: int = None,
        range_type: str = None,
        range_shape: str = None,
        duration_time: int = None,
        duration_type: str = None,
        casting_time: str = None,
        casting_type: str = None,
        db: Session = Depends(get_db)
):
    """
    Endpoint to filter and retrieve spell data based on specified parameters.

    Parameters:
    - `level` (int): Filter spells by their spell level.
    - `caster_class` (str): Filter spells based on the caster's class.
    - `school` (str): Filter spells by their school.
    - `damage_type` (str): Filter spells by their damage type.
    - `range_distance` (int): Filter spells by the range distance.
    - `range_type` (str): Filter spells by the range type.
    - `range_shape` (str): Filter spells by the range shape.
    - `duration_time` (int): Filter spells by the duration time.
    - `duration_type` (str): Filter spells by the duration type.
    - `casting_time` (str): Filter spells by the casting time.
    - `casting_type` (str): Filter spells by the casting type if you want to get spells that casts for bonus actiona
       `just enter bonus`.
    - `db` (Session): Dependency injection for the database session.

    Query Parameters:
    - `page` (int): Page number for paginated results (default: 1).
    - `page_size` (int): Number of items per page (default: 10).

    Example Usage:
    GET http://127.0.0.1:8000/data-filter/?duration_time=24&duration_type=hour&range_shape=point&range_type=feet&range_distance=30&casting_type=minute&casting_time=10
    Returns:
    - `status` (str): A string indicating the status of the request.
    - `data` (dict): A dictionary containing paginated results and metadata.
    """
    service_instance = Service()
    db_request = db.query(Spell, Durations, Ranges)  \
        .join(Durations, Durations.id == Spell.duration_id) \
        .join(Ranges, Ranges.id == Spell.spell_range_id)

    if level is not None:
        db_request = db_request.filter(Spell.spell_level == level)
    if school is not None:
        db_request = db_request.filter(Spell.school == school)
    if damage_type is not None:
        db_request = db_request.filter(Spell.damage_type == [damage_type])

    # filters if all ranges is passed
    if range_distance is not None and range_type is not None and range_shape is not None:
        db_request = db_request.filter(
            (Ranges.distance_range == range_distance) &
            (Ranges.distance_type == range_type) &
            (Ranges.shape == range_shape)
        )
    # if only range_shape and range_type is given as input
    elif range_distance is None and range_type is not None and range_shape is not None:
        db_request = db_request.filter(
            (Ranges.distance_type == range_type) &
            (Ranges.shape == range_shape)
        )
    elif range_distance is None and range_type is None and range_shape is not None:
        db_request = db_request.filter(
            Ranges.shape == range_shape
        )

    # Duration type because duration time is
    if duration_type is not None and duration_time is not None:
        db_request = db_request.filter(
            (Durations.duration_time == duration_time) &
            (Durations.duration_type == duration_type)
        )
    # if only duration time provided
    elif duration_time is None and duration_type is not None:
        db_request = db_request.filter(
            (Durations.duration_type == duration_type)
        )

    if casting_type is not None and casting_time is not None:
        db_request = db_request.filter(
            Spell.cast_time == service_instance.casting_type_for_comperation(casting_type, casting_time)
        )

    # Result formatting to suite response model
    print(db_request.all())

    if caster_class is not None:
        db_data = db.query(Spell.suitable_casters)
        print(db_data.all())
        formatted_result = [
            spell for spell, durations, ranges in db_request.all()
            if any(caster['name'] in spell.suitable_casters for caster in db_data)
        ]
    else:
        formatted_result = service_instance.format_result_for_all_spells(db_request.all())
        print(formatted_result)

    return {
        "status": "pussy test",
        "data": formatted_result
    }


"""
Registration and Log in 
"""


@app.post("/register/")
async def register():
    return responses.RedirectResponse("/?msg=sucsessfull", status_code=status.HTTP_201_CREATED)
