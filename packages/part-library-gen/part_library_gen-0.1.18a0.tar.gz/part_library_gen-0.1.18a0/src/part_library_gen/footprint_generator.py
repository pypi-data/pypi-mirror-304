from .generators.footprint_generator.tssop import generate as generate_tssop

generator_map = {
    "TSSOP": generate_tssop,
}


def generate(data):
    generator_name = data["generator"]
    generator = generator_map[generator_name]
    return generator(data, f"{generator_name}-{data["pin_count"]}")
