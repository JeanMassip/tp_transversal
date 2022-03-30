#!/bin/bash

openssl rsa -noout -text -inform PEM -in $1 -pubin
