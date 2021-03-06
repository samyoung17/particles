steps = 50;
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
        F(i,j) = f(r(i),s(j));
    end
end

%Trial different charge boundaries to find one enclosing 1 unit of charge
boundCharge = 1;
Finv = inv(F);
for k = 1:steps
    d = -b(1:k)';
    rho = Finv(1:k,1:k) * d;
    if sum(rho) > boundCharge
        break
    end
end
