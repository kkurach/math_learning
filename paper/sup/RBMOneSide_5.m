n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ 5;
end

optimized = 2^(n - 6) * (2 * ((sum((A' * sum((sum(A, 2) * (sum(A, 2) * A))', 1)), 1) * sum(A, 2))) + 20 * (sum(((sum(A, 2) * A)' * sum((A' * (A * A')), 1)), 1)) + -20 * ((((sum(A, 2) * A)' .* A')' * (A' .* A'))) + 30 * (sum((A' * (A * (A' * (A * A')))), 1)));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);