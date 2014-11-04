n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ 4;
end

optimized = 2^(n - 5) * (2 * ((sum((A' * sum((A' * sum(A', 1)), 1)), 1) * sum(A, 2))) + -4 * (((A' .* A')' * (A' .* A'))) + 6 * ((A * (A' * (A * A')))) + 12 * ((sum((A' * (A * A')), 1) * sum(A, 2))));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);