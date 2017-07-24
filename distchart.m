x = 0:delta:1;
y = vertcat(rho, zeros(steps +1 - length(rho),1));

plot(x,y)

