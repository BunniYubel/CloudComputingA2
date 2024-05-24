#!/bin/bash

# Delete all functions
for fn in $(fission fn list | awk 'NR>1 {print $1}'); do
    fission fn delete --name $fn
done

# Delete all packages
for pkg in $(fission pkg list | awk 'NR>1 {print $1}'); do
    fission pkg delete --name $pkg
done
