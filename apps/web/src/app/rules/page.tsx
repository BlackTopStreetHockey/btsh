"use client";
import Link from 'next/link';
import { Book } from 'lucide-react';
import { useState, useEffect } from 'react';

const Rules = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [activeSection, setActiveSection] = useState('');

    // Define all sections
    const sections = [
      { id: 'structure', title: 'STRUCTURE, OT, PLAY-OFFS, WEATHER' },
      { id: 'faceoffs', title: 'FACE-OFFS' },
      { id: 'bringing-ball', title: 'BRINGING A BALL INBOUNDS' },
      { id: 'goalie-safety', title: 'GOALIE SAFETY' },
      { id: 'ground-play', title: 'GROUND PLAY' },
      { id: 'goalies-balls', title: 'GOALIES AND BALLS' },
      { id: 'nets-creases', title: 'NETS – CREASES' },
      { id: 'stick-ball', title: 'STICK AND BALL PLAY' },
      { id: 'hand-body', title: 'HAND-BODY DEFLECTION' },
      { id: 'subs', title: 'SUBS' },
      { id: 'ref-interaction', title: 'REF INTERACTION AND REF SCHEDULING' },
      { id: 'teams', title: 'TEAMS' },
      { id: 'no-stick', title: 'NO STICK THROWING/SMASHING' },
      { id: 'penalties', title: 'PENALTIES' },
      { id: 'disciplinary', title: 'DISCIPLINARY COMMITTEE (DC)' },
      { id: 'prohibited', title: 'PROHIBITED ACTIONS' },
      { id: 'warnings', title: 'WARNINGS' },
      { id: 'falls', title: 'FALLS/INJURIES' },
      { id: 'chain', title: 'CHAIN OF COMMAND' },
      { id: 'bottom-line', title: 'THE BOTTOM LINE' },
    ];
  
    // Scroll to section handler
    const scrollToSection = (sectionId: string) => {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    };
  
    // Update active section based on scroll position
    useEffect(() => {
      const handleScroll = () => {
        const sectionElements = sections.map(section => ({
          id: section.id,
          element: document.getElementById(section.id)
        }));
  
        const currentSection = sectionElements.find(({ element }) => {
          if (!element) return false;
          const rect = element.getBoundingClientRect();
          return rect.top <= 100 && rect.bottom >= 100;
        });
  
        if (currentSection) {
          setActiveSection(currentSection.id);
        }
      };
  
      window.addEventListener('scroll', handleScroll);
      return () => window.removeEventListener('scroll', handleScroll);
    }, []);
  
    // Filter sections based on search
    const filteredSections = sections.filter(section => 
      section.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

  return (
    <section className="lg:mx-10 min-h-screen bg-gray-100">
      <div className="text-gray-900 py-8">
        <div className="container mx-auto flex flex-col items-start md:flex-row my-12 md:my-24">
          <div className="flex flex-col w-full sticky md:top-36 md:w-1/4 mt-2 md:mt-12 px-4">
            <h1 className="text-3xl md:text-4xl leading-normal md:leading-relaxed mb-2">Rules</h1>
            <p className="mb-4">Here are the latest and greatest rules.</p>
            <Link href="BTSH-Rules.pdf" className="flex gap-2 bg-blue-600 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-700">
              PDF Format <Book />
            </Link>

            <div className="my-4">
              <input
                type="text"
                placeholder="Search rules..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <nav className="mb-4 max-h-[60vh] overflow-y-auto bg-white border">
              {filteredSections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => scrollToSection(section.id)}
                  className={`block w-full text-left px-2 py-1 my-1 rounded hover:bg-gray-100 ${
                    activeSection === section.id ? 'bg-gray-100 font-semibold' : ''
                  }`}
                >
                  {section.title}
                </button>
              ))}
            </nav>
          </div>
          <div className="ml-0 md:ml-12 md:w-3/4">
            <div className="container mx-auto w-full h-full">
              <div className="relative wrap overflow-hidden p-8 h-full">
                <div className="w-full flex flex-col">
                  <small className="text-gray-600 italic mb-4">
                    (Last updated September 2022)
                  </small>
                  <p className="mb-2">
                    The BTSH rules are NOT necessarily the USA [BALL] HOCKEY rules, the NHL rules, or any other hockey
                    rules that you may be familiar with, but they are a collection of rules that have been patched
                    together to suit our needs. Read them, know them, live them!
                  </p>
                  <h2 id="structure" className="text-2xl font-bold mt-2">STRUCTURE, OT, PLAY-OFFS, WEATHER</h2>
                  <h4 className="text-xl font-bold">2.1 Game Structure</h4>
                  <p className="mb-2">
                    Games will start on time or within 5 minutes of the previous game ending. You should be arriving
                    before your game is slotted to start. If you have trouble doing this buy a new alarm clock. Teams
                    play with a max of 6 players on, including a goalie each. There must be at least two women on the
                    court at all times. Games are played in two 25-minute halves with a running clock. At the half the
                    teams switch sides. Teams always switch defending goals after each half but NOT after the second
                    half and before overtime. The clock is always stopped during water breaks and timeouts. If there
                    is a 1 or 2 goal differential (not tied, however) during the last two minutes of the second half-
                    the clock is stopped. If the game is tied or if there is a differential of 3 goals or more there
                    is no stoppage. The clock can also be stopped at the ref's discretion (ex. Medical needs). Each
                    team is permitted to take one thirty-second time out per game.{' '}
                  </p>
                  <p className="mb-2">
                    There is a maximum break of 2 minutes between halves, and between regulation and over-time. If the
                    gap in the score of the game reaches 10 goals, the game will end and will be declared a victory
                    for the team in the lead. This is called the outdated rule.
                  </p>
                  <h4 className="text-xl font-bold">2.2 Overtime (OT)</h4>
                  <p className="mb-2">
                    If the game is tied at the end of the 2nd half, a 5 minute sudden-death over-time (running clock)
                    will be played, wherein the first team to score wins and ends the game. The teams do not switch
                    sides for overtime. If a winner is not determined in the OT, a shootout commences. Shootouts: This
                    shoot out format will be followed for all regulation and playoff games (EXCEPT the semifinals and
                    the final) if no winner is declared in overtime. Teams will select 3 players to shoot, and at
                    least 1 of these 3 shooters must be female. If no winner is declared after each team&apos;s 3
                    shooters, teams will shoot back and forth in single rounds of sudden death until a winner is
                    declared. Shoot-Out Format past first 3 shooters: For every 3 shooters after the initial 3, at
                    least 1 must be female. Teams match the roster size and make-up of the smaller team. For example,
                    one team only has 3 women and the other team has 6, the team with 6 only has to have 3 of their
                    women shoot. Regarding your entire roster that day - all of your players have to shoot before you
                    can repeat a player (male or female), however, if one team has 10 people present and the other
                    team has 14, the team with 14 can repeat players after 10 shooters. If the shootout starts to
                    repeat shooters, teams will then be forced to ask themselves why they hate winning so badly.
                  </p>
                  <h4 className="text-xl font-bold">2.3 Play-off Selection/Structure</h4>
                  <p className="mb-2">
                    A player must play 6 regular season games for their team in order to be eligible to play in the
                    playoffs. (Unless this player is given prior approval by a majority of the captains before the
                    start of the playoffs.) The number of end of season exemption proposals (for playoff eligibility)
                    per team is limited to at most 2 players and 1 goalie per team. Teams are ranked 1 - 20 based on
                    Regular Season Schedule, regardless of division or conference. Playoff Weeks Playoffs Week 1 =
                    Bottom 8 teams square off to see which 4 will move onto to join Top 12 in the Round of 16.
                    Playoffs Week 2-Round of 16 = Top 12 plus 4 winners from Playoff Week 1 Playoffs Week 3 =
                    Quarterfinals Playoffs Week 4 = Semifinals Typical bracket system Playoffs Week 5 = Final Typical
                    bracket system There are 5 weeks of playoffs; there will be no double headers for any team except
                    if needed due to a prior playoff game being rained out. Eliminated Teams will have the option to
                    play exhibition games with games geared so that you face teams you missed in regular season, if
                    possible. Reseed every week. When selecting and ranking teams for play-off berths, teams will be
                    ranked by points. Teams tied for points will be ranked by the following criteria in the following
                    order: head-to-head wins between teams tied for points by total wins in the regular season by
                    greatest goal differential by coin toss, in which case the team that is alphabetically first gets
                    to call which side of the coin is in their favor sword fight. If the game is tied after the
                    regulation 50 minutes, then a ten-minute running-clock sudden-death over-time period will occur
                    (unlike the 5 minute clock for regular season). The first team to score in the OT period wins. If
                    the game is still tied at the end of the first over-time period, then a shoot-out will ensue, in
                    accordance with rule 2.2. In the event of overtime, unlike all other BTSH games, the semifinal
                    games and the final will never go to a shootout. Unlimited sudden-death overtime will occur until
                    one team scores. Overtime will occur in 25-minute periods, teams will switch sides after each
                    overtime period.
                  </p>
                  <h4 className="text-xl font-bold">2.4 Weather </h4>
                  <p className="mb-2">
                    If bad weather threatens to make playing conditions dangerous, then the League Manager and
                    Captains will work together make a decision about calling off games. They will attempt to make the
                    call no later than 2 hours prior to the scheduled start time of the game, One captain can
                    unilaterally postpone the game on their own without needing the other captain&apos;s approval so
                    long as it is at least 2 hours prior to gametime. If they try to cancel less than 2 hours prior to
                    game time and the other captain does not agree, both teams are still required to play. Not showing
                    up would result in a forfeit. Note: if the unilateral option becomes the standard and a team
                    abuses this, the team will forfeit the game. There has to actually be a weather concern. Also
                    please note that this is only dealing with postponing games before they start; this does not
                    include the situation where a game begins and then there is inclement weather.
                  </p>
                  <h2 id="faceoffs" className="text-2xl font-bold mt-2">FACE-OFFS</h2>
                  <p className="mb-2">
                    Face-offs occur at the center of the court/rink at the beginning of each period and after each
                    goal is scored. Refs have the discretion to call face-offs when play is stopped, and such
                    face-offs should occur near where play had stopped, unless otherwise provided for in these rules.
                    Players line up for face-offs behind the ball on the side of the court closest to their own goal
                    (on-sides). All face-offs shall be knock hockey style in which each player taking the face-off
                    must first hit the ground then each other's stick 3 times before making a play for the ball.
                  </p>
                  <h2 id="bringing-ball" className="text-2xl font-bold mt-2">BRINGING A BALL INBOUNDS</h2>
                  <p className="mb-2">
                    At any non-rink venue (without "boards" completely containing the playing surface): The ball must
                    be on or behind the out of bounds line when being brought in from the sidelines, then you bring it
                    back into bounds. The player in-bounding does not have to be behind the out-of- bounds line, only
                    the ball. The ball must be passed or shot into bounds; it cannot be carried in from out of bounds.
                    A player in-bounding the ball may shoot the ball anywhere within the playing area, INCLUDING ON
                    GOAL, directly or deflected. Opponents of players bringing a ball into bounds/goalies bringing
                    balls into play are to be no closer than 6 feet from the ball while the ball is being in-bounded
                    (that includes the player and his/her stick, of course).
                  </p>
                  <p className="mb-2">
                    Players, including goalies, have 5 seconds from the time the ball is set by the referee to bring
                    the ball into bounds or into play; if they do not bring the ball into play within 5 seconds the
                    referee may reverse possession. When the ball comes to rest in an area that is in-bounds but in or
                    near an obstruction which the referee considers problematic or potentially dangerous, then the
                    referee may stop play to conduct a face-off or the referee may give possession over to the first
                    player to contact the ball. When given possession, the ball is to be in- bounded from a spot
                    nearest to where it became unplayable. At a rink venue with continuous boards enclosing the
                    playing surface: When possession is given to a team, the ball must be introduced into play no
                    closer to the opponent's goal than the blue line nearest the opponent's goal. Opponents must not
                    be closer than 3 feet from the person "in- bounding" the ball. Once the in-bounder touches the
                    ball, it is in play. Thus, shots on goal from in-bounding at a rink venue are allowed. Inbounding
                    after ball leaves rink NOT over the sideline: The dugouts on the west court are out of bounds. Any
                    time the ball enters one of the 2 dugouts, the ref will blow the whistle immediately and
                    possession will change from the team who last touched the ball before it went into the dugout, to
                    the other team. (The same as out of bounds on the sideline) The team awarded the ball will inbound
                    it from the entrance to the dugout which the ball originally entered. The ref will start the
                    countdown from 5, the same as when a ball is inbounded from the sideline. Either door on the west
                    court: if the ball goes out of bounds, the possession will change to the team who did not touch it
                    last. The ball shall be inbounded from an area as close as possible to the point at which the ball
                    went out with the inbounding team receiving six feet from the defending team in order to play the
                    ball back in. The referee will give the standard 5 second count in which the ball must be played
                    before possession is changed. Turned up fences on any court: if the ball goes out of the court and
                    the referee can clearly determine the team the ball went off of, the opposite team shall inbound
                    the ball as close as possible to the location the ball went out and shall be afforded six feet of
                    room to bring the ball in. The referee will give the standard 5 second count in which the ball
                    must be played before possession is changed. Trees: If the ball hits any tree, it is not out of
                    play unless the following scenario occurs: the ball hits the tree above one of the goals, and
                    falls directly into the net without touching another player (other than the goalie -- basically,
                    if it falls of his or her back), that will not be counted as a goal. Otherwise, the game will not
                    be paused. If the referee cannot determine possession, then a faceoff shall occur at the closest
                    safe spot; the faceoff must occur between the two goal lines.
                  </p>
                  <h2 id="goalie-safety" className="text-2xl font-bold mt-2">GOALIE SAFETY</h2>
                  <p className="mb-2">
                    If an attacking player initiates any contact with a goalkeeper, incidental or otherwise, while the
                    goalkeeper is in the goal crease, and a goal is scored, the goal will be disallowed. If an
                    attacking player initiates any contact, other than incidental contact, with the goalkeeper, while
                    the goalkeeper is outside of the goal crease, and a goal is scored, the goal will be disallowed.
                    In all cases in which an attacking player initiates other than incidental contact with a
                    goalkeeper, whether or not the goalkeeper is inside or outside the goal crease, and whether or not
                    a goal is scored, this action will be considered a foul by the attacking player. If the goalie
                    initiates contact outside of the goal crease and a goal is scored, that goal is allowed. To sum
                    up: no touchee the goalie. Only goalies can call water breaks. Goalies can only call for water
                    breaks when their team has possession in their own zone or on a goalie ball (for either team).
                  </p>
                  <h2 id="ground-play" className="text-2xl font-bold mt-2">GROUND PLAY</h2>
                  <p className="mb-2">
                    Players may not lie on the ground to defend the goal and may not intentionally cover the ball to
                    prevent play. It's a chump move that causes more injuries than it's worth and is a punishable
                    offense. Any act which endangers other players, such as sliding, is not permitted. If such chump
                    moves occur, the offending player sits out a shift, and the opposing team gains possession from
                    the sidelines. A player may drop down to 1 or both knees in order to block a shot or an inbound.
                    However, the player must only drop down in a stationary position - again, NO sliding. Going down
                    to the knees is legal in BTSH and in most countries.
                  </p>
                  <h2 id="goalies-balls" className="text-2xl font-bold mt-2">GOALIES AND BALLS</h2>
                  <p className="mb-2">
                    Goalie throws are restricted to throws to the side or behind the goal line. Goalies cannot throw
                    the ball forward. Just noting this as they used to be able to. Get with the times, people. Goalies
                    may not cover, freeze, glove or close their hand on the ball unless they are within their crease
                    (fully or partially). Thus, goalies can't run to mid-court and cover the ball. Goalies may not
                    play the ball forward with their hand or glove (see above). If a goalie gloves or grabs the ball,
                    he or she has roughly three seconds to either drop it where they grabbed the ball or drop it
                    behind the goal line. If they hold on to the ball, the ball will be frozen and there will be a
                    whistle. The ball is frozen when the goalie covers the ball with his or her glove or any part of
                    their body and the ref determines that the goalie does not intend to play the ball further. At
                    this point the ref blows the whistle to stop play. After the whistle, the goalie must hand off the
                    ball to their defense behind the goal line. At this point the ref will begin counting down from 5
                    seconds until the player either passes the ball into play, or stickhandles across the plane of the
                    goal line. When the player does either of these two options, the ball is immediately
                    &ldquo;live&rdquo; and in play. The ball will also become "live" once the ref countdown reaches
                    zero and the other team can then cross the goal line to try and get the ball. To be clear- the
                    goalie can no longer play the ball forward; it must be dropped behind the goal line and restarted
                    by a teammate. When outside their crease, goalies are subject to all rules governing the play of
                    regular (non-goalie) players and may only play the ball with the stick and feet. This means they
                    cannot slide prone, raise their sticks above their waist, etc. Even while in the crease, the
                    goalie may not shoot/pass the ball above the cross bar or while playing the ball have their stick
                    go above their knee.
                  </p>
                  <h2 id="nets-creases" className="text-2xl font-bold mt-2">NETS – CREASES</h2>
                  <p className="mb-2">
                    Creases and nets shall be consistent at all playing locations. Goals are regulation 6-feet x
                    4-feet x 2-feet. Creases have a 4 foot radius from the center of the goal along the goal line. A
                    goal shall be disallowed if any body part of a member of the offending team is in or touching the
                    crease when the ball crosses the goal line. If a shoelace is on the tip of the crease the goal
                    will not be allowed. This rule is in effect to protect the goalies. Deal. No attacking player can
                    be in or have contact with the goal crease at any time, including their stick, except that a stick
                    is allowed to be inside the crease when the ball enters the crease as long as it is not making
                    contact with the goalie (see rule 5).
                  </p>
                  <h2 id="stick-ball" className="text-2xl font-bold mt-2">STICK AND BALL PLAY</h2>
                  <p className="mb-2">
                    In the interest of safety (preventing head/face injuries from high balls or sticks being swung at
                    high balls), the ball may not be shot into the air head high. If the ball is shot head high, it is
                    immediately whistled a dead ball with possession reversed at the nearest sideline from the spot of
                    the infraction. In other words- high balls are not delayed penalties. Exceptions to the rule
                    include a rising shot that travels head high beyond the net and deflected shots. In these
                    exception cases, play continues. In the case of a deflected shot that goes high, the ref should
                    use the deflection signal of one hand swiping over the other hand to indicate play carrying on and
                    yell "deflection" for clarity. Slap shots are illegal. A slap shot is loosely defined as winding
                    up or lifting your stick (in preparation for a shot) above knee level. (see rule 1 for further
                    clarification). The follow- through must not go above the waist. Players are not allowed to run
                    with their stick or play the ball with their stick above their waist. A goal scored by playing the
                    ball with a stick above the waist shall be disallowed. Stick checking is NOT allowed. Any play for
                    the ball must be just that; a play for the ball. You cannot lift the stick, hold the stick down,
                    or come down on the stick. A "sweep" for the ball is allowed.
                  </p>
                  <h2 id="hand-body" className="text-2xl font-bold mt-2">HAND-BODY DEFLECTION (SOME STOLEN FROM A LITTLE LEAGUE CALLED THE NHL)</h2>
                  <p className="mb-2">
                    If a ball is traveling off of the ground, a player shall be permitted to catch the ball out of the
                    air but must immediately place it or knock it down to the ground. He/she may not catch it and run
                    with it. A player shall be permitted to stop or "bat" a ball in the air with his/her open hand
                    unless, in the opinion of the ref, he/she has directed the puck to a teammate in any zone other
                    than the defending zone Play will not be stopped for any hand pass by players in their own
                    defending zone. A hand pass in the defending zone is considered to have occurred when both the
                    player making the pass AND the player receiving the pass have both of their feet inside their
                    defending zone. The defending zone is defined as the area closest to the team's defending goal up
                    to the mid-court face-off dot. Any attacking player who gloves the ball towards the goal keeper or
                    the net/crease area will be whistled for a hand pass. This will result in a goalie ball restart
                    for the defending team. A goal cannot be scored by an attacking player who bats or directs the
                    puck with his hand into the net. A goal cannot be scored by an attacking player who bats or
                    directs the puck and it is deflected into the net off any player, goalkeeper or official [or
                    tree]. When the puck enters the net on a clear unintentional deflection off a glove, the goal
                    shall be allowed. A goal cannot be scored by an attacking player who uses a distinct kicking
                    motion to propel the puck into the net. A goal cannot be scored by an attacking player who kicks a
                    puck that deflects into the net off any player, goalkeeper or official [or tree]. Any ball that is
                    directly deflected off or knocked in by a ref and goes in to the goal unobstructed shall not be
                    allowed.
                  </p>
                  <h2 id="subs" className="text-2xl font-bold mt-2">SUBS</h2>
                  <p className="mb-2">
                    Subs can enter the game at any time, however, no more than 6 players (including the goalie and 2
                    women) from any team can be playing on the court at any time. Subs may only shift on and off the
                    court when they are on the same half of the court as their team&apos;s &ldquo;bench&rdquo;. If a
                    player or team is caught shifting on/off on the other team&apos;s half, it is a delayed call for
                    Too Many Players and possession is given to the non-offending team.
                  </p>
                  <h2 id="ref-interaction" className="text-2xl font-bold mt-2">REF INTERACTION AND REF SCHEDULING</h2>
                  <p className="mb-2">
                    NO player may speak to the referees during the game, unless the referee initiates communication.
                    If you have something you think a referee should know, tell your captain and they will relay the
                    message to the referee at an opportune time. An opportune time includes after whistles or in
                    between halves, not during play. Keep in mind that the referee's call stands, so if you have a
                    dispute with a call, suck it up and shut up. Any attempt to yell, scream, bitch, whine, molest, or
                    otherwise annoy the ref will result in, first a warning to the player and the captain of the
                    players' team, then ejection from the game and possible DC committee action. (again, rule number
                    1.) Ref Schedulers and Ref Managers must not be members of the same team. If the ref
                    scheduler&apos;s team is in the semi-finals or finals they cannot have a role in scheduling refs
                    for those games. If this conflict of interest arises, the ref manager will assign refs. If both
                    have a conflict, then the commissioner will take over, followed by a randomly selected board
                    member.
                  </p>
                  <h2 id="teams" className="text-2xl font-bold mt-2">TEAMS</h2>
                  <p className="mb-2">
                    Teams are co-ed and must have at least two female players playing on the court at all times (not
                    including the goalie) or else they will need to play short. Rosters will be limited to 20 active
                    players plus 1 goalie and will be locked at the end of Week 15. Captains must submit a playoff
                    roster by this time and certify that all players on that roster have played at least 5 regular
                    season games. Captains are held responsible should a team be caught playing someone with less than
                    5 games experience. Exceptions may be granted by a majority vote of the captains. Beginning in
                    2019, refs will track attendance each week. Injured players who attend games will receive credit
                    for attendance and do not require an exception for the playoffs (assuming they met the 6 game
                    rule for a full season - updated to 5 games in 2022 on a shortened season). Players (FA or regular) must be a registered member of a team in order to accrue a game
                    played for that team. This means that FAs will no longer receive credit for games played on a team
                    until they formally join that team via their registration. This also means that any player, FA or
                    otherwise, who neglects to register with a team, may require an exemption at the end of the season
                    if they do not register timely and accrue the minimum required games played (6). Games will NOT
                    accrue retroactively if a player plays as a Free Agent and later registers with a team for which
                    they played games. In order for a player to accrue a game played, the player must have been
                    present for at least half of the game. Whether that means they show up for the entire second half,
                    only the first half or half of each half doesn&apos;t matter. If your team elects to use a player
                    from another BTSH team, the captain of the team you are playing that day must agree to this first.
                    If the other team&apos;s captain does not agree to this, you will need to either play shorthanded,
                    or forfeit. This goes for both players and goalies from other BTSH teams. Your team may use any
                    player who does not play for any BTSH team (except during playoffs) with no questions asked.
                    However, such players should register on the website as an FA before the game, just for
                    legal/liability reasons. During weeks 1-5 free agents can play as many games as they want,
                    afterwards they can only play 1 game max per week (exceptions are possible in the case of
                    goalie/female free agents). A game that is forfeited before it begins or because one team refuses
                    to play results in a score of 0 (zero) for the forfeiting team and at 10 (ten) for the
                    non-forfeiting team. If the game was in progress at the time it is declared forfeited, the score
                    shall be recorded as 0 (zero) for the loser and 1 (one), or such greater number of goals that had
                    been scored by it, for the winner. If a team does not have a goalie, a player on that team may
                    play in place of the goalie. If goalie equipment is not available, the player may not play as a
                    goalie and will be subject to player rules (6 players and no goalie on the court). A team may ask
                    another member of BTSH to play goal if it is first approved by the opposition's captain.
                  </p>
                  <h2 id="no-stick" className="text-2xl font-bold mt-2">NO STICK THROWING/SMASHING</h2>
                  <p className="mb-2">
                    No one is to ever smash a stick or anything else against the ground with force, and no one is ever
                    to throw a stick, on the court or off, because of the potential for severe injuries. Such
                    infractions may lead to penalties, ejection from the game or both.
                  </p>
                  <h2 id="penalties" className="text-2xl font-bold mt-2">PENALTIES</h2>
                  <p className="mb-2">
                    GAME RESTARTS AFTER A PENALTY OCCURS Should an infraction of the rules be committed by a player of
                    the team in possession and control of the puck, the Referee shall immediately stop play and assess
                    and the ball changes possession and ball is inbounded from sideline across from the point of the
                    foul. Should an infraction of the rules be committed by a player of a team NOT in possession and
                    control of the puck the Referee shall signal a delayed penalty. Play will be stopped immediately
                    when the offending team gains possession and control of the ball. The ball changes possession and
                    placed at the spot of the touchup. If any infraction of the rules is severe enough, intentional,
                    or repeated, the offending player will be written up by the head ref. A weekly review by the head
                    of officiating/DC director will then, based on the referees' write-ups, determine a penalty that
                    is suitable to the offense. If an offense is severe enough, items marked with a "(DC)" can be
                    brought up to the disciplinary committee (part 16) for further discipline and consequences,
                    including expulsion from the league.
                  </p>
                  <h4 className="text-xl font-bold">Minor offenses (written warning to 1 game suspension): </h4>
                  <ul className="list-disc pl-8">
                    <li>Holding </li>
                    <li>Hooking </li>
                    <li>Lofting </li>
                    <li>stick check </li>
                    <li>goalie covering out of crease </li>
                    <li>goalie delay of game </li>
                  </ul>
                  <h4 className="text-xl font-bold">Major offenses (written warning to 3 games suspension):</h4>
                  <ul className="list-disc pl-8">
                    <li>high sticking </li>
                    <li>slapshot</li>
                    <li>breaking Rule #1 (DC) </li>
                    <li>sliding (players AND goalies) </li>
                  </ul>
                  <h4 className="text-xl font-bold">Severe offenses (1 game – 5 game suspensions):</h4>
                  <ul className="list-disc pl-8">
                    <li>slashing (DC) </li>
                    <li>throwing/smashing stick (DC) </li>
                    <li>tripping (DC) </li>
                    <li>verbal abuse (DC) </li>
                  </ul>
                  <h4 className="text-xl font-bold">Extreme offenses (1 game suspension to season expulsion):</h4>
                  <ul className="list-disc pl-8">
                    <li>ref abuse </li>
                    <li>pushing/roughing/fighting </li>
                  </ul>
                  <p className="mb-2">
                    A 5-minute misconduct penalty can be given to any player who breaks Rule #1. This player must
                    leave the game for 5 minutes before they can return to the game, the ref will notify the team when
                    the 5 minutes is up. Infractions warranting a 5-minute misconduct include: any infraction which
                    takes away a golden scoring chance from the other team (for example, stick-checking someone from
                    behind while they are on a breakaway or stick-checking someone right in front of the net as they
                    are about to shoot) To reiterate- if a player commits a penalty against another player on a
                    breakaway-at least a 5 minute misconduct will be awarded. This call will be made in the interest
                    of safety and rule #1 verbal abuse of refs or other players Refs still have the option to say sit
                    a shift, sit the rest of the half, or sit the rest of the game (a game misconduct) for various
                    infractions. However, if a referee feels a player needs to sit longer than 5 minutes, or the whole
                    game, you do not necessarily need to give a 5-minute misconduct first.
                  </p>
                  <h2 id="disciplinary" className="text-2xl font-bold mt-2">DISCIPLINARY COMMITTEE (DC)</h2>
                  <p className="mb-2">
                    If a severe disciplinary infraction is committed and the head of officiating/DC director deems it
                    necessary, then the disciplinary committee (DC) will meet as soon as possible to deliberate on the
                    matter. The DC may also from time to time evaluate players with documented discipline problems.
                    The DC is comprised of a DC director who coordinates and initiates the meetings and the
                    representatives of the league teams (generally captains or proxy appointed by the team captain).
                    The DC director only votes to break a tie vote. The dc will have the authority to sanction players
                    with reprimand, game suspension, probation, or league expulsion. The DC is ultimately responsible
                    for upholding their decisions, and their decisions are final. Expelled players forfeit their fee
                    and must consider their expulsion permanent barring the discovery of new evidence or information
                    involving their expulsion. Only with such information can the player ask the DC to reexamine
                    his/her case and revote on his/her position in the league. Notice there are no jokes in this rule,
                    because we are dead serious. Best way to avoid the DC? <strong>See rule 1. </strong>
                  </p>
                  <h2 id="prohibited" className="text-2xl font-bold mt-2">PROHIBITED ACTIONS</h2>
                  <p className="mb-2">
                    This is a non-contact game where we chase an orange ball around the playground. As such, there is
                    no pushing or using physical force against another player. All players are responsible for being
                    in control of their actions at all times on the court and sidelines. Prohibited actions include
                    and are not limited to:
                  </p>
                  <ul className="list-disc pl-8">
                    <li>intentional physical contact with another player with your body or stick </li>
                    <li>checking</li>
                    <li>chopping (bring the stick down on another stick and also holding down a stick)</li>
                    <li>upward stick checking (flipping sticks up from behind and underneath) </li>
                    <li>hacking/slashing (shin- slapping) </li>
                    <li>tripping</li>
                    <li>hooking</li>
                    <li>spearing</li>
                    <li>stick end-butting </li>
                    <li>high sticking (stick above the waist) </li>
                    <li>vengeful shots made purely to induce injury </li>
                    <li>verbal taunts and abuse </li>
                    <li>fighting</li>
                  </ul>
                  <p className="mb-2">
                    any infraction covered by the <Link href="https://cdn1.sportngin.com/attachments/document/603a-2502129/2021-25_USAH_Playing_Rules.pdf" target="_blank">rules of USA Hockey</Link>, not stated above, and at the discretion of the
                    refs basically doing anything that would embarrass your loved ones. If you feel your temper
                    getting the best of you, take yourself out of the game before someone else does it for you.
                  </p>
                  <h2 id="warnings" className="text-2xl font-bold mt-2">WARNINGS</h2>
                  <p className="mb-2">
                    If you are repeatedly seen by or are reported to the referee as doing any of the above violent
                    no-nos, you will be given a warning and possibly sat down for a shift, 5 minutes, half, or ejected
                    from the game If the behavior continues, you may be suspended; you will have to appear in front of
                    the DC and possibly be ejected from the league.
                  </p>
                  <h2 id="falls" className="text-2xl font-bold mt-2">FALLS/INJURIES</h2>
                  <p className="mb-2">
                    If someone falls or trips or there is any safety issue, any player can ask the referee to call an
                    emergency time out until the situation is rectified.
                  </p>
                  <h2 id="chain" className="text-2xl font-bold mt-2">CHAIN OF COMMAND</h2>
                  <p className="mb-2">
                    Officials provide the final say in terms of goals and behavior on the court or rink, but the
                    players and captains are responsible for regulating themselves and those around them, and are
                    expected to do so in an adult manner. All decisions and behavior should keep player safety and
                    rule #1 in mind!!!!! If a player feels that he or she is being maliciously targeted by another
                    player, that player may bring the matter to the attention of their captain and the referee, but
                    may not retaliate.
                  </p>
                  <h2 id="bottom-line" className="text-2xl font-bold mt-2">THE BOTTOM LINE</h2>
                  <p className="mb-2">
                    These rules have been annually updated since the league's founding in 2000, and are tailored for a
                    low-key, fun, friendly, non-aggressive, social hockey league. Every player must know and follow
                    these rules. BTSH strives to be less than a "sports league" and more than a "social club," if that
                    makes any sense. It's not all about the wins, it's not all about the trophy, it IS all about
                    getting together with some friends and having FUN. Abiding by the rules in a strict manner will
                    help you accomplish that goal!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Rules;
