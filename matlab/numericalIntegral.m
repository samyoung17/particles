
f = @(x, r, s) s .* (r - s .* cos(x)) ./ (r.^2 + s.^2 - 2 .* r .* s .* cos(x)).^(3/2);
F = @(r,s) integral(@(x) f(x, r, s), 0, 2*pi);
Fanalytic = @(r,s)(2 * s/r * sign(r-s) * (ellipticE(-4*r*s/(r-s)^2)/(r+s) + ellipticK(-4*r*s/(r-s)^2)/(r-s)));

steps = 100;
delta = 1/steps;
r = 0:delta:1 - delta;
s = 1;

y = arrayfun(@(r_j) F(r_j,1), r);
yAnalytic = arrayfun(@(r_j) Fanalytic(r_j,1), r);
plot(r,y,r,yAnalytic);