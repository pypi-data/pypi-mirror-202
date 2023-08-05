

import argparse




def tune():
    # Grid search for hyper-parameters can be conducted by:
    #
    #    python -m freerec NAME_OF_EXPERIMENT CONFIG.yaml
    #
    from .parser import CoreParser
    from .launcher import Adapter
    cfg = CoreParser()
    cfg.compile()

    tuner = Adapter()
    tuner.compile(cfg)
    tuner.fit()


def make():
    from .data.preprocessing import datasets
    from .data.tags import USER, ITEM

    parser = argparse.ArgumentParser("Make Dataset")

    parser.add_argument("dataset", type=str, help="dataset name")
    parser.add_argument("--root", type=str, default=".", help="data")
    parser.add_argument("--filename", type=str, default=None, help="filename of Atomic files")

    parser.add_argument("--datatype", type=str, choices=('gen', 'seq'), default='gen')
    parser.add_argument("--by", type=str, choices=('ratio', 'last-two'), default='ratio')

    parser.add_argument("--star4pos", type=int, default=0)
    parser.add_argument("--kcore4user", type=int, default=10)
    parser.add_argument("--kcore4item", type=int, default=10)
    parser.add_argument("--ratios", type=str, default="8,1,1")

    parser.add_argument("--all", action="store_true", default=False)

    args = parser.parse_args()

    converter = getattr(datasets, args.dataset)(
        root=args.root,
        filename=args.filename
    )

    star4pos = args.star4pos
    kcore4user = args.kcore4user
    kcore4item = args.kcore4item
    ratios = tuple(map(int, args.ratios.split(',')))
    fields = None if args.all else (USER.name, ITEM.name)
    
    if args.datatype == 'gen' and args.by == 'ratio':
        converter.make_general_dataset(
            star4pos=star4pos,
            kcore4user=kcore4user,
            kcore4item=kcore4item,
            ratios=ratios,
            fields=fields
        )
    elif args.datatype == 'seq' and args.by == 'last-two':
        converter.make_sequential_dataset(
            star4pos=star4pos,
            kcore4user=kcore4user,
            kcore4item=kcore4item,
            fields=fields
        )
    elif args.datatype == 'seq' and args.by == 'ratio':
        converter.make_sequential_dataset_by_ratio(
            star4pos=star4pos,
            kcore4user=kcore4user,
            kcore4item=kcore4item,
            fields=fields
        )
    else:
        raise ValueError(f"`{args.datatype}' type dataset cannot be made by `{args.by}'")