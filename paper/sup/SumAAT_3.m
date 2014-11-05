n = 100;
m = 200;
A = randn(n, m);
original = sum(sum(((A * A') * A), 1), 2);

optimized = 1 * (sum((A * (sum(A, 2)' * A)'), 1));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);