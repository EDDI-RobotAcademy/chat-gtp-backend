#!/usr/bin/env bash

TEST_DIRS=$(find . -path ./.venv -prune -o -type d -name 'tests' -print)

source .venv/Scripts/activate

for TEST_DIR in $TEST_DIRS; do
  APP_NAME=$(basename $(dirname $TEST_DIR))
  TEST_FILES=$(find $TEST_DIR -type f -name 'test*.py')

  if [ -z "$TEST_FILES" ]; then
    echo "No test files found in $TEST_DIR"
    continue
  fi

  echo "Running tests for $APP_NAME"
  python manage.py test $APP_NAME.tests
done