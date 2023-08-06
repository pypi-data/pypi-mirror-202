#!/usr/bin/env python3


class Args:
    _args_apply_filter = ""
    _args_feed = ""
    _args_format = ""
    _args_invert = False
    # _args_list = False
    _args_pick_feeds = False

    @classmethod
    def define_args(cls, args):
        if args.apply_filter is not None:
            cls._args_apply_filter = args.apply_filter
        if args.feed is not None:
            cls._args_feed = args.feed
        if args.format is not None:
            cls._args_format = args.format
        cls._args_invert = args.invert
        # cls._args_list = args.list
        cls._args_pick_feeds = args.pick_feeds

    @classmethod
    def apply_filters(cls) -> str:
        return cls._args_apply_filter

    @classmethod
    def feed(cls) -> str:
        return cls._args_feed

    @classmethod
    def format(cls) -> str:
        return cls._args_format

    @classmethod
    def invert(cls) -> bool:
        return cls._args_invert

    # @classmethod
    # def list(cls) -> bool:
    #     return cls._args_list

    @classmethod
    def pick_feeds(cls) -> bool:
        return cls._args_pick_feeds
