n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ 6;
end

optimized = 2^(n - 7) * (2 * (sum(((sum(A, 2) * A)' * sum((A' * sum((sum(A, 2) * (sum(A, 2) * A))', 1)), 1)), 1)) + 30 * ((sum(((sum(A, 2) * A)' * sum((A' * (A * A')), 1)), 1) * sum(A, 2))) + 30 * ((A * (A' * (A * (A' * (A * A')))))) + -60 * ((A * (A' * ((A' .* A')' * (A' .* A'))))) + 90 * ((sum((A' * (A * (A' * (A * A')))), 1) * sum(A, 2))) + -60 * ((((sum(A, 2) * A)' .* A')' * ((sum(A, 2) * A)' .* A'))) + 32 * ((A * (((A' .* A')' .* (A' .* A')')' .* A'))));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);