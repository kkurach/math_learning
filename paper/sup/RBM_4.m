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
    original = original + (v * A * h') ^ 4;
  end
end

optimized = 2^(n + m - 9) * (24 * ((sum(A, 1) * ((A * sum(A, 1)')' * A)')) + 6 * (sum(((sum(A, 2) * (sum(A, 2)' * sum(A, 2)))' * A), 2)) + -24 * (sum(((A .* repmat(sum((A .* A), 1), n, 1)) * sum(A, 1)'), 1)) + 8 * (sum(sum((((A .* A) .* A) .* A), 1), 2)) + 12 * (sum(((sum(A, 2) * sum(sum((A .* A), 1), 2))' * A), 2)) + -24 * ((sum((A .* A), 2)' * sum((repmat(sum(A, 2), 1, m) .* A), 2))) + 12 * (sum(sum(((A * A') .* (A * A')), 1), 2)) + 12 * (sum((((sum(A, 2) * sum(sum(A, 1), 2)) * sum(sum(A, 1), 2))' * A), 2)) + -12 * ((sum((A .* A), 2)' * sum((A .* A), 2))) + -4 * (sum(((A .* repmat(sum(A, 1), n, 1)) * sum((A .* repmat(sum(A, 1), n, 1)), 1)'), 1)) + 24 * (sum(((A * (A' * sum(A, 2)))' * A), 2)) + 2 * ((((sum(sum(A, 1), 2) * sum(sum(A, 1), 2)) * sum(sum(A, 1), 2)) * sum(sum(A, 1), 2))) + 12 * ((sum(sum(((repmat(sum(sum(A, 1), 2), n, m) .* A) .* A), 1), 2) * sum(sum(A, 1), 2))) + 48 * (((sum(sum(A, 1), 2) * sum(A, 1)) * (A' * sum(A, 2)))) + 6 * ((sum(A, 1) * ((sum(A, 1)' * sum(A, 1)) * sum(A, 1)'))) + 6 * ((sum(sum((A .* A), 1), 2) * sum(sum((A .* A), 1), 2))) + 12 * ((sum(A, 1) * ((sum(A, 2)' * sum(A, 2)) * sum(A, 1))')) + 12 * ((sum(A, 1) * (sum(sum((A .* A), 1), 2) * sum(A, 1))')) + -12 * (sum(((A .* A) * sum((A .* A), 1)'), 1)) + 12 * (((sum(A, 1) * (sum(sum(A, 1), 2) * sum(A, 1))') * sum(sum(A, 1), 2))) + -4 * ((sum((repmat(sum(A, 2), 1, m) .* A), 2)' * sum((repmat(sum(A, 2), 1, m) .* A), 2))));
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);