# Security & Data Storage Documentation

## Overview

OIBSIP Task 5 is an educational real-time chat application.

The application implements basic security practices for user authentication and clearly documents how chat data is stored.

It is designed primarily for localhost use and is not intended to provide production-grade secure messaging.

---

## 1. Password Storage

User passwords are **not stored as plaintext**.

During registration, the application generates a random salt using Python's `secrets` module.

The password is processed using:

```text
PBKDF2-HMAC-SHA256