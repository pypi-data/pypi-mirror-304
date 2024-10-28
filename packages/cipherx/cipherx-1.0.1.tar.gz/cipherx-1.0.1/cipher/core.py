import hashlib

# Constants
BLOCK_SIZE = 16  # 128 bits
KEY_SIZE = 32    # 256 bits
NUM_ROUNDS = 10

# AES S-box
AES_S_BOX = [
    # 256-element list representing the AES S-box
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
    0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
    0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
    0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
    0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
    0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
    0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
    0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
    0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
    0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
    0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

# AES inverse S-box
AES_INV_S_BOX = [
    # 256-element list representing the inverse AES S-box
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38,
    0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87,
    0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D,
    0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2,
    0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA,
    0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A,
    0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02,
    0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA,
    0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85,
    0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89,
    0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20,
    0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31,
    0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D,
    0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0,
    0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26,
    0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
]

# Ensure the S-boxes are complete with 256 elements
assert len(AES_S_BOX) == 256
assert len(AES_INV_S_BOX) == 256

# Permutation layer
PERMUTATION = [
    0, 5, 10, 15, 4, 9, 14, 3,
    8, 13, 2, 7, 12, 1, 6, 11
]

def mul_by_2(num):
    """Multiply by 2 in GF(2^8)."""
    num = num & 0xFF
    return (((num << 1) ^ 0x1B) & 0xFF) if (num & 0x80) else (num << 1)

def mul_by_3(num):
    """Multiply by 3 in GF(2^8)."""
    return mul_by_2(num) ^ num

def mix_columns(state):
    """MixColumns operation over GF(2^8)."""
    for i in range(0, 16, 4):
        s0 = state[i]
        s1 = state[i+1]
        s2 = state[i+2]
        s3 = state[i+3]

        state[i]   = (mul_by_2(s0) ^ mul_by_3(s1) ^ s2 ^ s3) & 0xFF
        state[i+1] = (s0 ^ mul_by_2(s1) ^ mul_by_3(s2) ^ s3) & 0xFF
        state[i+2] = (s0 ^ s1 ^ mul_by_2(s2) ^ mul_by_3(s3)) & 0xFF
        state[i+3] = (mul_by_3(s0) ^ s1 ^ s2 ^ mul_by_2(s3)) & 0xFF
    return state

def inverse_mix_columns(state):
    """Inverse MixColumns operation over GF(2^8)."""
    for i in range(0, 16, 4):
        s0 = state[i]
        s1 = state[i+1]
        s2 = state[i+2]
        s3 = state[i+3]

        # Precomputed multiplication in GF(2^8) for the inverse matrix
        t0 = mul_by_14(s0) ^ mul_by_11(s1) ^ mul_by_13(s2) ^ mul_by_9(s3)
        t1 = mul_by_9(s0) ^ mul_by_14(s1) ^ mul_by_11(s2) ^ mul_by_13(s3)
        t2 = mul_by_13(s0) ^ mul_by_9(s1) ^ mul_by_14(s2) ^ mul_by_11(s3)
        t3 = mul_by_11(s0) ^ mul_by_13(s1) ^ mul_by_9(s2) ^ mul_by_14(s3)

        state[i]   = t0 & 0xFF
        state[i+1] = t1 & 0xFF
        state[i+2] = t2 & 0xFF
        state[i+3] = t3 & 0xFF
    return state

def mul_by_9(num):
    return mul_by_2(mul_by_2(mul_by_2(num))) ^ num

def mul_by_11(num):
    return mul_by_2(mul_by_2(mul_by_2(num))) ^ mul_by_2(num) ^ num

def mul_by_13(num):
    return mul_by_2(mul_by_2(mul_by_2(num))) ^ mul_by_2(mul_by_2(num)) ^ num

def mul_by_14(num):
    return mul_by_2(mul_by_2(mul_by_2(num))) ^ mul_by_2(mul_by_2(num)) ^ mul_by_2(num)

def key_schedule(key, num_rounds):
    """Generates round keys using SHA-256 and AES S-box."""
    round_keys = []
    for i in range(num_rounds + 1):
        data = key + i.to_bytes(4, 'big')
        hash_digest = hashlib.sha256(data).digest()
        round_key = list(hash_digest[:16])  # 128-bit round key
        # Apply S-box to the round key
        round_key = [AES_S_BOX[b] for b in round_key]
        round_keys.append(round_key)
    return round_keys

def generate_round_constants(num_rounds):
    """Generates round constants for each round."""
    round_constants = []
    for i in range(num_rounds):
        rc = hashlib.sha256(i.to_bytes(4, 'big') + b'round_constant').digest()
        round_constants.append(list(rc[:16]))  # 128-bit round constant
    return round_constants

def encrypt_block(plaintext_block, key, num_rounds=NUM_ROUNDS):
    """Encrypts a 128-bit block using the SPN structure."""
    state = list(plaintext_block)
    round_keys = key_schedule(key, num_rounds)
    round_constants = generate_round_constants(num_rounds)
    # Initial AddRoundKey
    state = [state[i] ^ round_keys[0][i] for i in range(16)]
    for i in range(1, num_rounds + 1):
        # SubBytes
        state = [AES_S_BOX[b] for b in state]
        # Permutation
        state = [state[PERMUTATION[j]] for j in range(16)]
        # MixColumns (skip in the last round)
        if i != num_rounds:
            state = mix_columns(state)
        # AddRoundKey and RoundConstant
        state = [state[j] ^ round_keys[i][j] ^ round_constants[i - 1][j] for j in range(16)]
    return bytes(state)

def decrypt_block(ciphertext_block, key, num_rounds=NUM_ROUNDS):
    """Decrypts a 128-bit block using the inverse SPN structure."""
    state = list(ciphertext_block)
    round_keys = key_schedule(key, num_rounds)
    round_constants = generate_round_constants(num_rounds)
    for i in reversed(range(1, num_rounds + 1)):
        # Undo AddRoundKey and RoundConstant
        state = [state[j] ^ round_keys[i][j] ^ round_constants[i - 1][j] for j in range(16)]
        # Undo MixColumns (skip in the first decryption round)
        if i != num_rounds:
            state = inverse_mix_columns(state)
        # Undo Permutation
        inv_perm = [PERMUTATION.index(j) for j in range(16)]
        state = [state[inv_perm[j]] for j in range(16)]
        # Undo SubBytes
        state = [AES_INV_S_BOX[b] for b in state]
    # Final AddRoundKey
    state = [state[i] ^ round_keys[0][i] for i in range(16)]
    return bytes(state)

def pad_data(data):
    """Applies PKCS#7 padding."""
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad_data(data):
    """Removes PKCS#7 padding."""
    padding_len = data[-1]
    if padding_len < 1 or padding_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length.")
    if data[-padding_len:] != bytes([padding_len] * padding_len):
        raise ValueError("Invalid padding.")
    return data[:-padding_len]

def encrypt(data, key):
    """Encrypts data using the block cipher in ECB mode."""
    data = pad_data(data)
    ciphertext = b''
    if len(key) != KEY_SIZE:
        raise ValueError(f"Key must be {KEY_SIZE} bytes long.")
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        encrypted_block = encrypt_block(block, key)
        ciphertext += encrypted_block
    return ciphertext

def decrypt(ciphertext, key):
    """Decrypts data using the block cipher in ECB mode."""
    plaintext = b''
    if len(key) != KEY_SIZE:
        raise ValueError(f"Key must be {KEY_SIZE} bytes long.")
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted_block = decrypt_block(block, key)
        plaintext += decrypted_block
    return unpad_data(plaintext)

def main():
    key = b'supersecretkeythatis32byteslong!'  # Exactly 32 bytes long

    print("Custom SPN Encryption and Decryption")
    print("Using a fixed 256-bit key for demonstration purposes.")
    print(f"Key: {key.decode('utf-8')}\n")

    # Ask the user to input a plaintext message
    plaintext = input("Enter a plaintext message to encrypt: ")

    # Display the plaintext
    print(f"\nPlaintext Message: {plaintext}")

    # Encrypt the message
    plaintext_bytes = plaintext.encode('utf-8')
    ciphertext = encrypt(plaintext_bytes, key)
    ciphertext_hex = ciphertext.hex()
    print(f"\nEncrypted Message (hex): {ciphertext_hex}")

    # Decrypt the message
    decrypted_bytes = decrypt(ciphertext, key)
    decrypted_message = decrypted_bytes.decode('utf-8')
    print(f"\nDecrypted Message: {decrypted_message}")

    # Verify that the decrypted message matches the original
    if decrypted_message == plaintext:
        print("\nSuccess: Decrypted message matches the original message.")
    else:
        print("\nFailure: Decrypted message does not match the original message.")

if __name__ == "__main__":
    main()