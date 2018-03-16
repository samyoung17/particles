function y = f(r,s)
    if r == s
        y = pi / r^2;
    else
        y = (2 * s/r * sign(r-s) * (ellipticE(-4*r*s/(r-s)^2)/(r+s) + ellipticK(-4*r*s/(r-s)^2)/(r-s)));
    end
end
