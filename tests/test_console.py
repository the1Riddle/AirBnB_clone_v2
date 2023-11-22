#!/usr/bin/python3

"""unittests for console.py."""
import os
import unittest
import models
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """test setup"""
        cls.consol = HBNBCommand()

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_emptyline(self):
        """Test if cmd is empty """
        with patch('sys.stdin', StringIO('\n')):
            with self.assertRaises(SystemExit) as cm:
                self.consol.cmdloop()

        self.assertEqual(str(cm.exception), 'None')

    def test_create(self):
        """Test create method"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", mock_stdout.getvalue())

        """Test create command with an invalid class name"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.consol.onecmd("create InvalidClass")
            output = mock_stdout.getvalue().strip()
            self.assertEqual("** class doesn't exist **", output)

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
               "** class name missing **\n", f.getvalue())

        """Destroying an object without providing a class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        """Destroying an obj with a class name, but not an ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User 1")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """tests all cmd inputs"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all")
            self.assertEqual(
                "[]\n", f.getvalue())
