import logging
logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d:%H:%M:%S',
                level=logging.ERROR)
mfl = logging.getLogger("pymfx4")
mfl.setLevel(logging.ERROR)
#ch = logging.StreamHandler()
#ch.setLevel(logging.WARNING)
#form = logging.Formatter('%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
#mfl setFormatter()


