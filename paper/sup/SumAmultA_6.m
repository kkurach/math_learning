n = 100;
m = 200;
A = randn(n, m);
original = sum(sum((((((A * A') * (A .* A)) * A') * (A .* A)) * A'), 1), 2);

optimized = 1 * (sum((sum(((repmat(sum((repmat(sum(((repmat(sum((repmat(sum(A, 1), n, 1) .* A)', 1)', 1, m) .* A) .* A), 1), n, 1) .* A)', 1)', 1, m) .* A) .* A), 1)' .* sum(A, 1)'), 1));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);