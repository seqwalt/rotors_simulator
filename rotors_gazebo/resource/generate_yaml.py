#!/usr/bin/env python3

import yaml
pos_mult = 0.3;
lin_vel_mult = 1.0;
ang_mult = 0.4;
ang_vel_mult = 1.0;

data = {
'position_gain': {'x': 4*pos_mult, 'y': 4*pos_mult, 'z': 4*pos_mult},
'velocity_gain': {'x': 2.2*lin_vel_mult, 'y': 2.2*lin_vel_mult, 'z': 2.2*lin_vel_mult},
'attitude_gain': {'x': 0.7*ang_mult, 'y': 0.7*ang_mult, 'z': 0.035*ang_mult},
'angular_rate_gain': {'x': 0.1*ang_vel_mult, 'y': 0.1*ang_vel_mult, 'z': 0.025*ang_vel_mult}
}

file = 'lee_controller_generated.yaml'
stream = open(file, 'w')
yaml.dump(data, stream)
print('YAML file generated')
