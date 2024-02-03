import json
import os

# Used to make this work when importing JsonParser
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

"""
If you decide to use this parser please initiate 
a class with inputing a path to your index.json
like in this example = JsonParser('./path/to/your/index.json')
after that you are welcome to use it but do not forget 
to store spells_fson folder in same folder as your parser
"""


class JsonParser:

    def __init__(self, index_file):
        """
        :param index_file:
        get all files path from index.json file
        and converts them to  accessible dict from any other function
        dict: key(book_name) value current path to book.json
        """
        self.json_files = dict()
        self.wanted_data = [
                            'name', 'source', 'page', 'level', 'school', 'entries', 'damageInflict',
                            'time', 'range', 'components', 'duration', 'entriesHigherLevel'
                            ]
        with open(index_file, 'r') as opened_index:
            for key, value in json.load(opened_index).items():
                self.json_files[key] = f"./spells_json/{value}"

    def __json_filter(self, json_data, book_name=None):
        """
        :param json_data:
        :param book_name:
        :return result as dict with all needed data:
        """
        result = dict()
        # looks for wanted data in json that was passed to filter
        for key, value in json_data.items():
            # if key is in wanted data list than its appends to
            if key in self.wanted_data:
                result[key] = value
                if key == 'name':
                    with open('./spells_json/sources.json', 'r') as opened_json:
                        data = json.load(opened_json)
                        try:
                            result['class'] = data[book_name][value]['class']
                        except KeyError:
                            result['class'] = [{
                                                "name": "Wizard",
                                                "source": "PHB"
                                                }]
                else:
                    pass
        return result

    def __get_ranges(self):
        """
        Get all ranges from all spell file
        :param self.json_files:
        :return a list of unique spell ranges:
        """
        unique_ranges = []

        for json_file in self.json_files.values():
            with open(json_file, 'r') as open_json_file:
                for spell in json.load(open_json_file).get('spell', []):
                    range_dict = spell.get('range')
                    if range_dict is not None:
                        # Convert the dictionary to a JSON string for comparison
                        range_str = json.dumps(range_dict, sort_keys=True)

                        # Check if the JSON string is already in unique_ranges
                        if range_str not in [json.dumps(r, sort_keys=True) for r in unique_ranges]:
                            unique_ranges.append(range_dict)

        return unique_ranges

    def __get_durations(self):
        """
		Get all durations from all spell file
		:param self.json_files:
		:return: list of dictionaries containing unique durations
		"""
        unique_durations = []

        for json_file in self.json_files.values():
            with open(json_file, 'r') as open_json_file:
                for spell in json.load(open_json_file).get('spell'):
                    duration_dict = spell.get('duration')
                    if duration_dict is not None:
                        # Convert the dictionary to a JSON string for comparison
                        range_str = json.dumps(duration_dict, sort_keys=True)

                        # Check if the JSON string is already in unique_durations
                        if range_str not in [json.dumps(r, sort_keys=True) for r in unique_durations]:
                            unique_durations.append(duration_dict)
        return unique_durations

    def __get_spells(self):
        """
        :return:
        """
        # Creating all hashed lists that will be used
        hashed_sources = []
        hashed_ranges = []
        hashed_durations = []
        for source in self.json_files.keys():
            hashed_sources.append(hash(source))
        for range in self.__get_ranges():
            hashed_ranges.append(hash(str(range)))
        for duration in self.__get_durations():
            hashed_durations.append(hash(str(duration)))

        # Create list spells
        spell_list = list()
        for key, json_file in self.json_files.items():
            with open(json_file, 'r') as open_json_file:
                for spell in json.load(open_json_file).get('spell'):
                    spell_list.append(self.__json_filter(spell, key))

        # Change source, range, duration to corresponding foreign key
        for spell in spell_list:
            if hash(spell['source']) in hashed_sources:
                spell['source'] = hashed_sources.index(hash(spell['source'])) + 1

            if hash(str(spell['range'])) in hashed_ranges:
                spell['range'] = hashed_ranges.index(hash(str(spell['range']))) + 1

            if hash(str(spell['duration'])) in hashed_durations:
                spell['duration'] = hashed_durations.index(hash(str(spell['duration']))) + 1

        return spell_list
    def get_all_sources(self):
        """
        returns all sources for easy input to database with sqlalchemy
		:return only keys from json_file as list of dictionaries:
		"""
        result = []
        for book_name in self.json_files.keys():
            result.append({'book_name': book_name})

        return result

    def get_all_ranges(self):

        result = []
        for item in self.__get_ranges():
            if item['type'] != 'special':
                result.append({
                                'shape':          item['type'],
                                'distance_type':  item['distance'].get('type'),
                                'distance_range': item['distance'].get('amount')
                                })
            else:
                result.append({
                                'shape': item['type'],
                })
        return result


    def get_all_durations(self):
        """
        :return list of dict in format that easy to input into sqlalchemy insert statement:
        """
        result = []
        for value in self.__get_durations():
            if value[0]['type'] == 'timed':
                # appending dictionary with proper key names and values from original source
                result.append({
                               "duration_type": value[0]['duration']['type'],
                               "duration_time": value[0]['duration']['amount'],
                               "concentration": value[-1].get('concentration', False)
                               })
            else:
                result.append({
                    "duration_type": value[0]['type'],
                    "duration_time": 'Null',
                    "concentration": value[-1].get('concentration', False)
                })
        return result

    def get_all_spells(self):
        result = []
        for spell in self.__get_spells():
            result.append({
                            "spell_name":           spell['name'],
                            "book_page":            spell['page'],
                            "spell_level":          spell['level'],
                            "school":               spell['school'],
                            "cast_time":            spell['time'],
                            "components":           spell['components'],
                            "spell_description":    spell['entries'],
                            "suitable_casters":     spell['class'],
                            "entries_higher_level": spell.get('entriesHigherLevel', None),
                            "damage_type":          spell.get('damageInflict', None),
                            "source_id":            spell['source'],
                            "spell_range_id":       spell['range'],
                            "duration_id":          spell['duration']
                            })
        return result


get_data = JsonParser('spells_json/index.json')
get_data.get_all_durations()
