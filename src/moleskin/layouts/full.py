from moleskin.layout import Layout


class FullLayout(Layout):
    def arrange(self, surface, child_sizes):
        return surface.get_size(), ((0, 0),) * len(child_sizes)


__all__ = ['FullLayout']
