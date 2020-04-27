#!/bin/bash

# Simple script to send an email to a specified address with the content of a specified file
mail -s 'Reminder!' $1  < $2
