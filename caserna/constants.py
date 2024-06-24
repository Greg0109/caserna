#!/usr/bin/env python3
"""
Script to hold some constants
"""
import os
POSTGRES_USER = os.environ.get('GF_DATABASE_USER', '')
POSTGRES_PASSWORD = os.environ.get('GF_DATABASE_PASSWORD', '')
POSTGRES_DB = os.environ.get('GF_DATABASE_DB', '')
POSTGRES_HOST = os.environ.get('GF_DATABASE_HOST', '')
POSTGRES_PORT = os.environ.get('GF_DATABASE_PORT', '')
