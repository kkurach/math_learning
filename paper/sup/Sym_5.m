n = 1;
m = 18;
A = randn(1, m);
sub = nchoosek(1:m, 5);
original = 0;
for i = 1:size(sub, 1)
  original = original + prod(A(sub(i, :)));
end

optimized = (-10 * (sum((repmat(sum((A' .* repmat(sum((repmat(sum((A' .* A'), 1), 1, m) .* A), 2), m, 1)), 1), 1, m) .* A), 2)) + -20 * (sum((((repmat(sum((A' .* A'), 1), 1, m) .* A)' .* A')' .* A), 2)) + 15 * (sum((repmat(sum(((repmat(sum((A' .* A'), 1), 1, m) .* A)' .* A'), 1), 1, m) .* A), 2)) + 24 * (sum(((((A' .* A')' .* A)' .* A')' .* A), 2)) + 20 * (sum((repmat(sum((A' .* repmat(sum(((A' .* A')' .* A), 2), m, 1)), 1), 1, m) .* A), 2)) + 1 * (sum((A' .* repmat(sum((repmat(sum((A' .* repmat(sum((repmat(sum(A', 1), 1, m) .* A), 2), m, 1)), 1), 1, m) .* A), 2), m, 1)), 1)) + -30 * (sum((repmat(sum((((A' .* A')' .* A)' .* A'), 1), 1, m) .* A), 2))) / 120;
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);