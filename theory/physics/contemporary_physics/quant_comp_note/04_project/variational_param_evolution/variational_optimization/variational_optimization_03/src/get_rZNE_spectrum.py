import asyncio


from get_ZNE_val import get_gs_ZNE, get_bell_ZNE
from get_rZNE_val import get_rZNE_vals


IDEAL_BELL_VAL = -12.0


async def get_rZNE_spectrum(
    s_ls,
    direct_optimizer,
    slsqp_optimizer,
    n_list,
    ideal_bell_val=IDEAL_BELL_VAL,
    chip="qiskit_aer",
    chip_options=None,
):

    # redefine chip_options for each s
    chip_options_ls = []
    for s in s_ls:
        opts = None
        if chip_options is not None:
            opts = dict(chip_options)
            opts["name"] = f"{opts.get('name', 'my_job')}_s={s:.2f}"
        chip_options_ls.append(opts)

    # get ZNE spectrum
    bell_zne_records = await asyncio.gather(
        *(
            get_bell_ZNE(
                s_ls[s_idx], n_list, chip=chip, chip_options=chip_options_ls[s_idx]
            )
            for s_idx in range(len(s_ls))
        )
    )
    gs_zne_records = await asyncio.gather(
        *(
            get_gs_ZNE(
                s_ls[s_idx],
                direct_optimizer,
                slsqp_optimizer,
                n_list,
                chip=chip,
                chip_options=chip_options_ls[s_idx],
            )
            for s_idx in range(len(s_ls))
        )
    )

    # get rZNE spectrum
    bell_rzne_records = await asyncio.gather(
        *(
            get_rZNE_vals(bell_zne_records[s_idx], ideal_val=ideal_bell_val, r=None)
            for s_idx in range(len(s_ls))
        )
    )
    gs_rzne_records = await asyncio.gather(
        *(
            get_rZNE_vals(
                gs_zne_records[s_idx],
                ideal_val=None,
                r=bell_rzne_records[s_idx]["r"],
            )
            for s_idx in range(len(s_ls))
        )
    )

    return gs_rzne_records, bell_rzne_records
