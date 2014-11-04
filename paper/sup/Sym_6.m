n = 1;
m = 18;
A = randn(1, m);
sub = nchoosek(1:m, 6);
original = 0;
for i = 1:size(sub, 1)
  original = original + prod(A(sub(i, :)));
end

optimized = (24 * (sum((repmat(sum((((A .* A)' .* (A .* A)') .* A')', 2), 1, m) .* A), 2)) + -5 / 2 * (sum(((repmat(sum(((repmat(sum((A .* A), 2), 1, m) .* A) .* A), 2), 1, m) .* A) .* A), 2)) + 20 / 3 * (sum(((repmat(sum(((A' .* A') .* A')', 2), 1, m) .* A)' .* (A .* A)')', 2)) + -20 * (sum((((A' .* A') .* A')' .* ((A' .* A') .* A')'), 2)) + 15 * (sum(((repmat(sum(((A .* A)' .* (A .* A)')', 2), 1, m) .* A) .* A), 2)) + -20 * (sum((repmat(sum(((repmat(sum((A .* A), 2), 1, m) .* A)' .* (A .* A)')', 2), 1, m) .* A), 2)) + -15 * (sum((repmat(sum(A, 2), 1, m) .* (repmat(sum(((A .* A)' .* (A .* A)')', 2), 1, m) .* A)), 2)) + 15 / 2 * (sum((repmat(sum((repmat(sum(((repmat(sum((A .* A), 2), 1, m) .* A) .* A), 2), 1, m) .* A), 2), 1, m) .* A), 2)) + 1 / 6 * (sum((repmat(sum((repmat(sum((repmat(sum((repmat(sum(A, 2), 1, m) .* (repmat(sum(A, 2), 1, m) .* A)), 2), 1, m) .* A), 2), 1, m) .* A), 2), 1, m) .* A), 2)) + 20 / 3 * (sum(((repmat(sum((repmat(sum(A, 2), 1, m) .* (repmat(sum(A, 2), 1, m) .* A)), 2), 1, m) .* A)' .* (A .* A)')', 2)) + -5 / 2 * (sum((repmat(sum(((repmat(sum((repmat(sum(A, 2), 1, m) .* (repmat(sum(A, 2), 1, m) .* A)), 2), 1, m) .* A) .* A), 2), 1, m) .* A), 2))) / 120;
normalization = sum(abs(original(:)));
assert(sum(abs(original(:) - optimized(:))) / normalization < 1e-10);