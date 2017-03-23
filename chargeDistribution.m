steps = 20;
delta = (1/steps);
% Set r as the midpoints of the annuli
r = (0:delta:(1-delta)) + delta/2;
s = (0:delta:(1-delta)) + delta/2;

%Calculate the bounding force
b = arrayfun(@(r_j) f(r_j,1), r);

%Calculate the outward force on a point at radius r due to a ring with
%radius s
F = zeros(steps, steps);
for i = 1:steps
    for j = 1:steps
        F(i,j) = f(r(j),s(i));
    end
end

%Trial different charge boundaries to find one enclosing 1 unit of charge
Finv = inv(F);

a = arrayfun(@(r_j) areaOfAnAnnulus(r_j,delta), r);
rho=0;
for k = 1:steps
    d = vertcat(-b(1:k)',zeros(steps - k,1));
    rho = Finv * d;
    q = a * rho;
    if q > 1
        break
    end
end

function y = f(r,s)
    if r == s
        y = pi / r^2;
    else
        y = s/r * (-ellipticK(r*s) + -((r-s)/(r+s)) * ellipticE(r*s));
    end
end

function a = areaOfAnAnnulus(r, delta)
    a = pi * ((r + delta)^2 - (r-delta)^2);
end