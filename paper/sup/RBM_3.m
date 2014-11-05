n = 7;
m = 8;
A = randn(n, m);
nset = dec2bin(0:(2^(n) - 1));
mset = dec2bin(0:(2^(m) - 1));
original = 0;
for i = 1:size(nset, 1)
  for j = 1:size(mset, 1)
    v = logical(nset(i, :) - '0');
    h = logical(mset(j, :) - '0');
    original = original + (v * A * h') ^ 3;
  end
end

optimized = 2^(n + m - 7) * (12 * (sum(sum((A .* repmat(sum((A .* repmat(sum(A', 2)', n, 1)), 2), 1, m)), 1), 2)) + 2 * (sum(sum((A .* repmat(sum((sum(A', 1) .* repmat(sum(sum(A', 1)', 1), 1, n)), 2), n, m)), 1), 2)) + 6 * (sum(sum((A .* repmat(sum((sum(A', 1) .* sum(A', 1)), 2), n, m)), 1), 2)) + 6 * (sum(sum(((repmat(sum(sum(A', 1)', 1), n, m) .* A)' .* A'), 1), 2)) + 6 * (sum(sum((A .* repmat(sum((repmat(sum(sum(A', 1)', 1), n, m) .* A), 1), n, 1)), 1), 2)));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);