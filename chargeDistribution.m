steps = 10;
delta = (1/steps);
r = delta:delta:1;
s = delta:delta:1;

b = arrayfun(@(r_j) f(r_j,1), r);
F = zeros(steps, steps);
for i = 1:steps
    for j = 1:steps
        F(i,j) = f(r(j),s(i));
    end
end

F
plot(r_vec, B);

function y = f(r,s)
y = (2*s/r) * (ellipticE(-4*r*s/(r-s)^2)/(r+s) + ellipticK(-4*r*s/(r-s)^2)/(r-s));
end