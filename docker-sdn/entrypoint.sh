#!/usr/bin/env bash

service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640

# Execute any command passed to the entrypoint (e.g., "/bin/bash")
exec "$@"

service openvswitch-switch stop