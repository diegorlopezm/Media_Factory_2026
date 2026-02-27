class StatsManager:
    def __init__(self):
        # Ahora la lista de personajes vive en el objeto (self)
        self.characters_found = []
        self.number_of_characters = 0
    def add_character(self, name):
        # Convertimos el nombre a minúsculas para facilitar la comparación
        name = name.lower()
        # Añadimos el personaje a la lista persistente del objeto
        if "character" in name and "no character" not in name:
            self.characters_found.append(name)
            print(f"Personaje añadido: {name}")
            self.number_of_characters += 1
        else:
            print(f"Not a character")


# Simulación de uso
manager = StatsManager()

# --- MEGA-DATASET: 100 ENTRADAS PARA MEDIA FACTORY ---
data_entries = [
    "character, Russell Crowe as Enoc, dirty face, cinematic lighting, gladiator armor",
    "landscape, vast desert, sand dunes, heat haze, no characters",
    "female character, Tifa Lockhart, fighting stance, 8k, realistic",
    "character, Sephiroth, silver hair, masamune sword, fire background",
    "close up, rtx 5090 gpu, circuit board, neon lights, no characters",
    "multiple characters, group of rebels, urban warfare, debris",
    "solitary character, man in cloak, walking towards a portal, fantasy",
    "interior, futuristic laboratory, glass tanks, blue liquid, no character found",
    "character, Cloud Strife, buster sword, motorcycle, mid-gar city",
    "forest, ancient trees, sunlight beams, mossy rocks, no characters present",
    "main character, Enoc, looking at the horizon, dramatic sky, cape",
    "landscape, alien planet, purple sky, floating islands, no character",
    "two characters, Aerith and Zack, church background, flowers, soft light",
    "character, Vincent Valentine, red cloak, golden gun, dark aesthetic",
    "tech demo, unreal engine 5, nanite rocks, lumen lighting, no characters",
    "character, Jill Valentine, blue top, stars uniform, raccoon city, zombies",
    "horror scene, abandoned hospital, blood on walls, flickering light, no character found",
    "character, Leon S. Kennedy, leather jacket, police badge, dark forest",
    "mountain range, snowy peaks, eagle flying, cold atmosphere, no characters",
    "character, Barret Wallace, gatling gun arm, angry expression, industrial",
    "underwater, coral reef, shark, bubbles, deep sea, no characters",
    "character, Yuffie Kisaragi, materia in hand, ninja outfit, cheerful",
    "cyberpunk alley, rain, neon signs, trash cans, steam, no character found",
    "character, Cid Highwind, goggles, cigar, spear, airship pilot",
    "volcano interior, lava, obsidian, smoke, intense heat, no characters",
    "multiple characters, Turks in suits, dark sunglasses, helicopter",
    "landscape, autumn forest, orange leaves, river, no character present",
    "character, Red XIII, flaming tail, canyon background, tribal tattoos",
    "spaceship cockpit, stars visible, control panels, no character found",
    "character, Albert Wesker, black trench coat, sunglasses, virus vial",
    "temple ruins, vines, stone statues, mystical fog, no characters",
    "character, Lady Dimitrescu, tall woman, white dress, castle, horror",
    "beach, blue water, palm trees, white sand, sunny day, no characters",
    "character, Carlos Oliveira, assault rifle, tactical vest, umbrella corp",
    "server room, blinking lights, cooling fans, rtx 5090 racks, no character",
    "character, Claire Redfield, red jacket, motorcycle, shotgun",
    "glacier, ice caves, blue light, frozen lake, no characters",
    "character, Rufus Shinra, white suit, arrogant look, corporate office",
    "swamp, dark water, dead trees, fireflies, murky, no character found",
    "character, Hojo, scientist lab coat, creepy smile, experiments",
    "prairie, tall grass, wind blowing, wildflowers, no characters",
    "character, Reno, red hair, electro-mag rod, smirk",
    "medieval village, marketplace, empty stalls, cobblestone, no character",
    "character, Rude, bald head, sunglasses, stoic expression",
    "canyon, red rocks, blue sky, dry bushes, no characters",
    "character, Elena, blonde hair, suit, rookie member",
    "industrial zone, pipes, rust, steam vents, heavy machinery, no characters",
    "character, Biggs and Wedge, rebel uniforms, sector 7",
    "flower garden, Aerith's house, peaceful, butterflies, no character found",
    "character, Jessie Rasberry, tech gear, smiling, explosives",
    "void, space, nebula, galaxies, infinite, no characters",
    "character, Dyne, gun arm, desert robes, tragic look",
    "station, train tracks, graffiti, urban decay, no character",
    "character, Marlene, small girl, innocent, bar background",
    "ocean wave, massive, blue water, foam, splash, no characters",
    "character, Lucrecia Crescent, crystal cave, sad expression",
    "wheat field, golden hour, farmhouse, no character present",
    "character, Kadaj, twin blade, motorcycle, advent children style",
    "library, old books, candles, dust motes, no characters",
    "character, Loz and Yazoo, silver hair, fast movement",
    "cave, stalactites, glowing mushrooms, dark, no character found",
    "character, Genesis Rhapsodos, red armor, black wing, book in hand",
    "waterfall, jungle, tropical birds, mist, no characters",
    "character, Angeal Hewley, buster sword, mentor, serious face",
    "sky, clouds, sunset, orange and pink, no characters",
    "character, Nero the Sable, dark energy, mechanical wings",
    "moonlight, full moon, clouds, night sky, no character found",
    "character, Weiss the Immaculate, white hair, dual swords, psycho",
    "field, green grass, blue sky, sheep, peaceful, no characters",
    "character, Shelke the Transparent, glowing sticks, tech suit",
    "bridge, golden gate style, fog, suspension cables, no characters",
    "character, Shalua Rui, artificial arm, scientist gear",
    "cliff, ocean view, crashing waves, seagulls, no character present",
    "character, Azul the Cerulean, massive build, heavy weapon",
    "desert oasis, palm trees, water, sand, no characters",
    "character, Rosso the Crimson, red outfit, dual blades, fierce",
    "tundra, permafrost, moss, cold, no character found",
    "character, Minerva, goddess armor, glowing light, majestic",
    "road, highway, night, car lights, long exposure, no characters",
    "character, Cait Sith, cat on a giant moogle, megaphone",
    "market, spices, colorful rugs, crowd, no character",
    "character, Moogle, kupo, small creature, flying",
    "ruins, coliseum, stone pillars, sand, no character found",
    "character, Chocobo, yellow feathers, bird, riding",
    "garden, zen stones, raked sand, bonsai, no characters",
    "character, Cactuar, green cactus, 1000 needles pose",
    "meadow, flowers, mountains, sunny, no character present",
    "character, Tonberry, lantern, knife, small hood",
    "cliffside, sunset, ocean, dramatic, no character",
    "character, Bahamut, dragon, wings spread, megaflare",
    "cityscape, skyscrapers, glass, steel, no characters",
    "character, Ifrit, fire demon, horns, muscular",
    "winter, snow, ice, cold, no character found",
    "character, Shiva, ice goddess, blue skin, elegant",
    "sunset, purple sky, silhouette of trees, no characters",
    "character, Ramuh, old man, lightning staff, beard",
    "canyon, deep, shadows, rocks, no character",
    "character, Leviathan, sea serpent, water dragon",
    "valley, green, river, peace, no character found",
    "character, Odin, knight on horse, zantetsuken sword"
]

for name in data_entries:
    manager.add_character(name)

print(f"Total de personajes encontrados: {manager.number_of_characters}")