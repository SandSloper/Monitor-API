#!/bin/sh
gunicorn -c ./gunicorn.conf app:app
