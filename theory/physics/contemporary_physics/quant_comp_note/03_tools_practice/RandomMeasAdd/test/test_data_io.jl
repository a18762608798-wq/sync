using RandomMeasAdd

N = 8
site_indices = siteinds("Qubit", N);

test_index = 1

if test_index == 1
    group_path = joinpath(@__DIR__, "data", "aer-independence_pauli_setting0_settings27_shots1024.npz")
    permuted_order = [1, 2, 3, 4];
    permuted_group, permuted_indices = import_permuted_group(
        group_path, site_indices, permuted_order
    )
elseif test_index == 2
    pauli_path = "./04_workflow/b_data_acquisition/reflect_pauli_group.npz"
    permuted_order = [3, 6, 4, 5];
    res, bases = import_permuted_pauli(
        pauli_path, permuted_order
    );
elseif test_index == 3
    pauli_path = "./04_workflow/b_data_acquisition/purity_pauli_group.npz"
    permuted_order = [3, 6, 4, 5];
    res, bases = import_permuted_pauli(
        pauli_path, permuted_order
    );
end
