$fa = 1;
$fs = 0.4;

puck_diameter = 77;
puck_height = 26;
_puck_radius = puck_diameter / 2;

leg_height = 95;
leg_diameter = 60;
_leg_radius = leg_diameter / 2;

thickness = _puck_radius - _leg_radius;

_epsilon = 0.001;

difference() {
    cylinder(h=puck_height+leg_height, r=_puck_radius+thickness);
    translate([0, 0, -_epsilon])
        cylinder(h=puck_height+2*_epsilon, r=_puck_radius);
    translate([0, 0, puck_height-_epsilon])
        cylinder(h=leg_height+2*_epsilon, r=_leg_radius);
}
