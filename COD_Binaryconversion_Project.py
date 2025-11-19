import struct

def float_to_bits_native(x, precision='single'):
    """Return bitstring and hex for float x.
    precision: 'single' (32-bit) or 'double' (64-bit)
    """
    if precision == 'single':
        packed = struct.pack('!f', float(x))        # network(big)-endian
        bits = ''.join(f'{b:08b}' for b in packed)
        hx = packed.hex()
    elif precision == 'double':
        packed = struct.pack('!d', float(x))
        bits = ''.join(f'{b:08b}' for b in packed)
        hx = packed.hex()
    else:
        raise ValueError("precision must be 'single' or 'double'")
    return bits, hx

# Example quick usage
for val in [0.15625, -13.625, 1.0e-40, float('inf'), float('nan'), 0.0, -0.0]:
    bits32, hx32 = float_to_bits_native(val, 'single')
    bits64, hx64 = float_to_bits_native(val, 'double')
    print(f"{val!r}\n  32-bit: {bits32}  hex: {hx32}\n  64-bit: {bits64}  hex: {hx64}\n")
