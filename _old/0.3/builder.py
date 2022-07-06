"""
Open Project Guidebook builder v0.3
"""
from dataStructure import Area, Subarea, Boulder, Route, Variation, Photo

if __name__ == '__main__':

    bookPhotos = {
        'octurnal': Photo(
            name='octurnal',
            fileName='Octurnal.jpg',
            description='Carson landing the big throw on Octurnal. Classic!'),
        'smackdown': Photo(
            name='smackdown',
            fileName='Smackdown.jpg',
            description='Andrew posting up at the start of Smackdown'),
    }
    bookAreas = {
        'garden': Area('The Garden Main')
    }
    bookSubAreas = {
        'fightClub': Subarea('Fight Club', bookAreas['garden']),
        'methLab': Subarea('Meth Lab', bookAreas['garden'])
    }
    bookBoulders = {
        'miniMe': Boulder(
            name='Mini Me',
            parent=bookSubAreas['fightClub']),
        'fightClub': Boulder(
            name='Fight Club',
            parent=bookSubAreas['fightClub']),
        'methLab': Boulder(
            name='Meth Lab',
            parent=bookSubAreas['methLab'],
            photos=[
                bookPhotos['octurnal'],
                bookPhotos['smackdown'],
            ]
        ),
        'enchilada': Boulder(
            name='Enchilada',
            parent=bookSubAreas['methLab']),
    }
    bookRoutes = {
        'austinPowers': Route(
            name='Austin Powers',
            parent=bookBoulders['miniMe'],
            grade=5,
            description='start on blunt arete. Make tricky moves to lip and traverse left into top of Dr. Evil'),
        'drEvil': Route(
            name='Dr. Evil',
            parent=bookBoulders['miniMe'], grade=3,
            description='sit start on lowest holds of a compressiony arete with left foot over a small rock. '
                        'Pull some tricky moves to gain better holds.'),
        'fightClub': Route(
            name='Fight Club',
            parent=bookBoulders['fightClub'],
            grade=8,
            description='Area classic, this rig is a feather in any would be crushers cap. Start on the far right arete as for Ear. '
                        'Traverse across the angle change and top out above a bubbly crimp rail on the overhanging face.'),
        'fightClubLeft': Route(
            name='Fight Club Left',
            parent=bookBoulders['fightClub'],
            grade=9,
            description='The trickier left side of the fight club boulder may still be unsent (who knows). Start low on the left arete '
                        'of the overhang and crank on obvious breaky holds out right to the crimp rail of Fight Club. Top as for Fight Club'),
        'octurnal': Route(
            name='Octurnal',
            parent=bookBoulders['methLab'],
            grade=7,
            description='Originally known as Tom\'s phsychadelic trip. For many this is the local test piece in the area. Start sitting '
                        'with left hand on a sloping triangular rib and right hand on a slopey cripm at the arete. Crank a few hard '
                        'moves to gain the lip then traverse left through the lightning bolt hold to a pumpy top out. Full Value'),
        'smackdown': Route(
            name='Smackdown',
            parent=bookBoulders['methLab'],
            grade=7,
            description='Start standing with left hand gaston and right hand jug sidepull. Crank some powerful moves on bad feet '
                        'and follow the line of crimps to a top out left'),
        'enchilada': Route(
            name='Enchilada',
            parent=bookBoulders['enchilada'],
            grade=9,
            description='Start matched on a good flat rail low to the ground with some awkward feet options. Cross into a '
                        'comfortable crimp and fire up left before coming back right to a flat jug. Pretty classic as far as low balls go!'),
    }
    bookVariations = {
        'number2': Variation(
            name='Number 2',
            parent=bookRoutes['drEvil'],
            grade=3,
            description='start as for Dr. Evil but roll onto the slab right of the arete using a good crimp rail'),
        'mrBigglesworth': Variation(
            name='Mr. Bigglesworth',
            parent=bookRoutes['drEvil'],
            grade=1,
            description='Stand start variation of Number 2. Start on good crimps right of the arete just before the angle change.'),
        'mole': Variation(
            name='Mole',
            parent=bookRoutes['drEvil'],
            grade=1,
            description='Stand start as for Mr. Bigglesworth but climb the arete as for Dr. Evil.'),
        'octurnalDirect': Variation(
            name='Direct Exit',
            parent=bookRoutes['octurnal'],
            grade=7,
            description='Of all the Octurnal exits this one has the most interesting move. Climb Octurnal to the ledge '
                        'then pull some tricky moves to round the right arete. Continue on through a heads up top out.'),
        'octurnalCenter': Variation(
            name='Center Exit',
            parent=bookRoutes['octurnal'],
            grade=7,
            description='The easiest top option for this boulder involves pulling through a suprisingly good side pull '
                        'above the left end of the ledge. For years this variation livided in moss covered obscurity '
                        'climbing it will make you wonder why the awkward pumpfest traverse exit is the default line'),
        'harborFreight': Variation(
            name='Harbor Freight',
            parent=bookRoutes['smackdown'],
            grade=8,
            description='Sit down start at the lowest available holds and climb into Smackdown. This was literally '
                        'unearthed when a local climber yarded a large rock out from the landing of Smackdown using a '
                        'chain and come along. The device broke in the process inspiring the name of the route.'),
    }

    print('DEEZ NUTZ')
    print(bookBoulders['fightClub'].routes)
