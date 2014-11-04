n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ 8;
end

optimized = 2^(n - 9) * (420 * ((sum(((sum(A, 2) * A)' * sum((A' * (A * (A' * (A * A')))), 1)), 1) * sum(A, 2))) + 56 * ((sum(((sum(A, 2) * A)' * sum(((sum(A, 2) * A)' * sum((A' * (A * A')), 1)), 1)), 1) * sum(A, 2))) + 896 * ((A * (A' * (A * (((A' .* A')' .* (A' .* A')')' .* A'))))) + 2 * (sum(((sum(A, 2) * A)' * sum(((sum(A, 2) * A)' * sum((A' * sum((sum(A, 2) * (sum(A, 2) * A))', 1)), 1)), 1)), 1)) + -544 * ((A * ((((A' .* A')' .* (A' .* A')')' .* A')' .* (A' .* A')')')) + 210 * ((A * (A' * (A * (A' * (A * (A' * (A * A')))))))) + 896 * ((A * ((((sum(A, 2) * A)' .* A')' .* ((sum(A, 2) * A)' .* A')')' .* A'))) + -1680 * ((A * (A' * (((sum(A, 2) * A)' .* A')' * ((sum(A, 2) * A)' .* A'))))) + 280 * ((A * ((A' * ((A' .* A')' * (A' .* A')))' .* (A' .* A')')')) + 840 * ((sum((A' * (A * (A' * (A * (A' * (A * A')))))), 1) * sum(A, 2))) + -280 * ((((sum(A, 2) * (sum(A, 2) * A))' .* A')' * ((sum(A, 2) * (sum(A, 2) * A))' .* A'))) + -840 * ((A * (A' * (A * (A' * ((A' .* A')' * (A' .* A'))))))));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);