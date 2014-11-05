n = 14;
m = 1;
A = randn(1, n);
nset = dec2bin(0:(2^(n) - 1));
original = 0;
for i = 1:size(nset, 1)
  v = logical(nset(i, :) - '0');
  original = original + (v * A') ^ 8;
end

optimized = 2^(n - 9) * (56 * (((((((A * (sum(A, 2) * A)') * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2))) + 2 * ((((((((sum(A, 2) * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2))) + 210 * ((((A * (sum((A .* A), 2) * A)') * sum((A .* A), 2)) * sum((A .* A), 2))) + 896 * (((((A' .* (A .* A)')' * (A' .* (A .* A)')) * sum(A, 2)) * sum(A, 2))) + 420 * ((((((A * (sum((A .* A), 2) * A)') * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2))) + -544 * (((A .* A) * ((A' .* (A .* A)')' .* (A' .* (A .* A)')')')) + 896 * ((((A' .* (A .* A)')' * (A' .* (A .* A)')) * sum((A .* A), 2))) + -1680 * ((((((A .* A) * (A .* A)') * sum((A .* A), 2)) * sum(A, 2)) * sum(A, 2))) + 280 * ((((A .* A) * (A .* A)') * ((A .* A) * (A .* A)'))) + 840 * (((((A * (sum((A .* A), 2) * A)') * sum((A .* A), 2)) * sum(A, 2)) * sum(A, 2))) + -280 * (((((((A .* A) * (A .* A)') * sum(A, 2)) * sum(A, 2)) * sum(A, 2)) * sum(A, 2))) + -840 * (((((A .* A) * (A .* A)') * sum((A .* A), 2)) * sum((A .* A), 2))));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);