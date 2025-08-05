# Educational Password Cracking Tool

A comprehensive Python-based educational tool for demonstrating password cracking techniques using wordlist attacks. This tool is designed specifically for cybersecurity education and authorized penetration testing.

## 🎯 Purpose

This tool demonstrates how weak passwords can be cracked using dictionary attacks, teaching the importance of using strong, unique passwords for cybersecurity.

## ✨ Features

- **Multiple Hash Algorithm Support**: MD5, SHA-1, and SHA-256
- **Paste-Friendly Interface**: Easy hash input with automatic type detection
- **Real-Time Progress**: Live statistics and cracking progress
- **Rich Console Output**: Beautiful CLI interface (with fallback for basic terminals)
- **Comprehensive Wordlist**: Supports custom wordlists
- **Command-Line Options**: Full automation support
- **Educational Focus**: Built-in disclaimers and responsible use guidelines

## 📋 Requirements

- Python 3.7 or higher
- `rich` library (optional, but recommended for enhanced display)

## 🚀 Installation

1. Download the complete package
2. Install dependencies:
   ```bash
   pip install rich
   ```
3. Ensure you have a wordlist file (like `rockyou.txt`)

## 💻 Usage

### Interactive Mode
```bash
python password_cracker.py
```

### Command Line Mode
```bash
# Basic usage with MD5 hash
python password_cracker.py --hash-type 1 --target e10adc3949ba59abbe56e057f20f883e

# With custom wordlist and verbose output
python password_cracker.py --wordlist /path/to/wordlist.txt --verbose

# SHA-256 hash example
python password_cracker.py --hash-type 3 --target 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

### Command Line Options

- `--hash-type {1,2,3}`: Hash algorithm (1=MD5, 2=SHA-1, 3=SHA-256)
- `--target HASH`: Target hash to crack
- `--wordlist PATH`: Path to wordlist file (default: rockyou.txt)
- `--verbose`: Enable detailed progress information

## 📁 File Structure

```
password-cracker/
├── password_cracker.py    # Main application (standalone)
├── README.md             # This file
├── rockyou.txt                   # Wordlist file (user-provided)
```

## 🎓 Educational Objectives

- Understand password hashing algorithms (MD5, SHA-1, SHA-256)
- Learn about wordlist/dictionary attacks
- See real-time password cracking statistics
- Appreciate the importance of strong password policies
- Understand cybersecurity concepts through hands-on experience

## 🔧 Technical Details

### Hash Algorithms Supported
- **MD5**: 128-bit hash (32 hex characters) - Fast but cryptographically weak
- **SHA-1**: 160-bit hash (40 hex characters) - Deprecated but still encountered
- **SHA-256**: 256-bit hash (64 hex characters) - Secure and widely used

### Performance
- Optimized for educational use with real-time statistics
- Handles large wordlists efficiently
- Memory-efficient streaming approach
- Cross-platform compatibility

### Security Features
- Built-in legal disclaimers
- Responsible use enforcement
- Educational context framing
- No network communication
- Local file processing only

## 🛡️ Legal Disclaimer

**⚠️ This tool is for educational purposes and authorized security testing only.**

### Authorized Uses:
- Learning about password security and hashing
- Authorized penetration testing with proper permissions
- Educational cybersecurity training
- Testing your own systems and passwords

### Prohibited Uses:
- Cracking passwords without explicit authorization
- Any illegal or malicious activities
- Unauthorized access to systems or accounts

**By using this tool, you agree to use it responsibly and in compliance with all applicable laws.**

## 🔍 Example Hashes for Testing

Here are some common passwords and their hashes for educational testing:

### MD5 Hashes (32 characters):
- `123456`: `e10adc3949ba59abbe56e057f20f883e`
- `password`: `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`
- `admin`: `21232f297a57a5a743894a0e4a801fc3`

### SHA-1 Hashes (40 characters):
- `123456`: `7c4a8d09ca3762af61e59520943dc26494f8941b`
- `password`: `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8`
- `admin`: `d033e22ae348aeb5660fc2140aec35850c4da997`

### SHA-256 Hashes (64 characters):
- `123456`: `8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`
- `password`: `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`
- `admin`: `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918`

## 🔗 Wordlist Sources

For educational purposes, you can use various wordlist sources:

- **RockYou.txt**: Classic password list from the RockYou breach
- **SecLists**: Comprehensive collection of security-related lists
- **Custom Lists**: Create your own based on specific scenarios

## 🐛 Troubleshooting

### Common Issues:

1. **"rich library not found"**
   - Solution: `pip install rich` or use basic mode

2. **"Wordlist file not found"**
   - Solution: Ensure rockyou.txt is in the same directory or specify correct path

3. **"Invalid hash format"**
   - Solution: Ensure hash is hexadecimal and proper length

4. **Permission denied**
   - Solution: Check file permissions on wordlist

## 📚 Additional Resources

- [OWASP Password Guidelines](https://owasp.org/www-community/vulnerabilities/Weak_Passwords)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Password Security Best Practices](https://www.cisa.gov/password-security)

## 🤝 Contributing

This is an educational tool. Contributions should focus on:
- Educational value enhancement
- Code clarity and documentation
- Security best practices
- Performance improvements
- Cross-platform compatibility

## 📄 License

This tool is provided for educational purposes. Users are responsible for compliance with applicable laws and regulations.

---

**Remember**: The best defense against password attacks is using strong, unique passwords and implementing proper security practices!
