scene_prompt = """Given the object {object}, please provide a list of scenes where this object is most likely to be found. 
Focus only on the following potential locations: Living Room, Bedroom, Kitchen, Office, and Store. 
**Please respond strictly in the following format: ["Scene1", "Scene2", "Scene3"]**. 
Exclude any explanations, lists, or additional text. Only include the scenes where the object's presence is probable, ordered from most likely to less likely."""

material_prompt = """Given the object {object}, please provide a list of possible surface materials for this object. 
Only include materials that are commonly used for this type of object. 
**Please respond strictly in the following format: ["Material1", "Material2", "Material3"]**. 
Exclude any explanations, lists, or additional text. Only include the materials that are probable."""

fuzzy_name_prompt = """Given the object {object}, please provide a list of alternative names or synonyms that are semantically related to this object. 
Focus on names that reflect its characteristics, usage, or common associations. 
Provide a minimum of three names, but if there are strong semantic associations, aim to provide up to ten names. If the associations are weak, feel free to provide fewer than ten. 
**Please respond strictly in the following format: ["Name1", "Name2", "Name3", "Name4", "Name5"]**. 
Exclude any explanations, lists, or additional text. Only include names that are significantly relevant."""

mass_prompt = """Given the following object {object} with {volume} cubic meters,
estimate the mass in kilograms. Provide only the numerical value as output, without any additional text. 
For example, if the estimated mass is 2 kg, just output: 2."""

friction_coefficient_prompt = """Given the following object {object}, estimate the surface friction coefficient based on its typical use and the most common materials associated with it, such as wood, metal, plastic, or rubber. 
Consider the object's typical conditions and the interaction it has with surfaces. The coefficient should be a decimal value between 0.05 and 1, rounded to two decimal places. 
Provide only the numerical value as output, without any additional text."""

spatial_prompt = """For the object "{object}", respond strictly with two one-dimensional arrays:
- First array for "Parent" objects. "Parent" objects are those on which the given object is commonly placed. Provide a realistic list of "Parent" objects without any repetition.
- Second array for "Child" objects. "Child" objects are those that can be placed on top of the given object. Provide a realistic list of "Child" objects without any repetition.
Ensure that the objects listed are relevant and applicable in real-world scenarios. Avoid any repeated entries and aim for a sufficient variety.
Only return the two arrays, without any additional formatting or text. Do not combine them into a single array.
**Please respond strictly in the following format: ["Parent1", "Parent2", "Parent3"], ["Child1", "Child2", "Child3"]**."""

asset_name_prompt = """What is the object in the image? Respond with just one word: the object's name."""