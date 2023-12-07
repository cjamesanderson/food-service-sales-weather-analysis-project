function mu = intervalMean(v, int_length)
%INTERVALMEAN Compute the mean of elements vector v over the interval int_length

% Initialize some useful values
m = length(v);
mu = zeros(size(v));
queue = [];

for i = 1:m
  queue = [queue; v(i)];
  if length(queue) > int_length
    queue = queue(2:end);
  end
  mu(i) = mean(queue);
end
