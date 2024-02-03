from sqlalchemy import asc, desc
from fastapi import HTTPException
from database import models
import json

class Service:
    def __init__(self):
        pass

    @staticmethod
    def format_result_for_all_spells(data):
        formatted_result = [
            {
                "id": spell.id,
                "name": spell.spell_name,
                "level": spell.spell_level,
                "components": spell.components,
                # Duration type, time, concentration
                "duration": {
                    "type": duration.duration_type,
                    "time": duration.duration_time,
                    "concentration": duration.concentration
                },
                "time": spell.cast_time,
                # Range with
                "ranges": {
                    "type": ranges.shape,
                    "distance": {
                        "type": ranges.distance_type,
                        "amount": ranges.distance_range
                    }
                }
            }
            for spell, duration, ranges in data
        ]
        return formatted_result

    @staticmethod
    def format_spell(data):
        formatted_result = [
            {
                "id": spell.id,
                "name": spell.spell_name,
                "source": source,
                "page": spell.book_page,
                "level": spell.spell_level,
                "school": spell.school,
                "components": spell.components,
                # Duration type, time, concentration
                "duration": {
                    "type": duration.duration_type,
                    "time": duration.duration_time,
                    "concentration": duration.concentration
                },
                "time": spell.cast_time,
                # Range with
                "ranges": {
                    "type": ranges.shape,
                    "distance": {
                        "type": ranges.distance_type,
                        "amount": ranges.distance_range
                    }
                },
                "casters": spell.suitable_casters,
                "description": spell.spell_description,
                "descriptionOnHigherLevels": spell.entries_higher_level
            }
            for spell, source, duration, ranges in data
        ]
        return formatted_result

    @staticmethod
    def casting_type_for_comperation(casting_type, casting_time):
        return json.dumps([{"number": int(casting_time), "unit": casting_type}])

    def apply_sort(self, result, filter_name, asc_value):
        filter_mapping = {
            "lvl": (
                result.order_by,
                (asc(models.Spell.spell_level) if asc_value else
                 desc(models.Spell.spell_level)
                 ,)
            ),
            "name": (
                result.order_by,
                (asc(models.Spell.spell_name) if asc_value else
                 desc(models.Spell.spell_name)
                 ,)
            ),
            "concentration": (
                result.order_by,
                (asc(models.Durations.concentration) if asc_value else
                 desc(models.Durations.concentration)
                 ,)
            ),
            "duration": (
                result.order_by,
                (asc(models.Durations.duration_time) if asc_value else
                 desc(models.Durations.duration_time),
                 desc(models.Durations.duration_type)
                 ),
            ),
            "time": (
                result.order_by,
                (asc(models.Spell.cast_time) if asc_value else
                 desc(models.Spell.cast_time)
                 ,)
            ),
            "range": (
                result.order_by,
                (asc(models.Ranges.distance_range) if asc_value else
                 desc(models.Ranges.distance_range),
                 desc(models.Durations.duration_type)
                 ),
            )
        }

        if filter_name not in filter_mapping:
            raise HTTPException(status_code=400, detail="Invalid filter parameter")

        operation, args = filter_mapping[filter_name]
        result = operation(*args)

        return self.format_result_for_all_spells(result)

