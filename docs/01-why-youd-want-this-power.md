# Why You'd Want This Power

## The Problem

Something invisible arrives — in a lightning bolt, in a frog's leg that twitches when touched with two different metals, in the spark that jumps from your finger to a doorknob. Three phenomena, seemingly unrelated. Could one thing explain all of them?

In 1791 Luigi Galvani touched a dissected frog's leg with a copper hook resting on an iron railing. The leg kicked — without any muscle signal, without any animal willing it. He called it "animal electricity." Alessandro Volta disagreed: the source wasn't the frog, it was the two different metals. But both men agreed something was moving, and it could do mechanical work.

Your problem is simpler but harder: you've identified something that seems to explain all three phenomena. How do you use it? You can't use what you can't measure. You can't control what you can't describe.

Any description must satisfy:

- Explains why sparks, shocks, twitching muscles, and heat from a wire all seem related
- Gives at least two independent quantities — enough to tell the difference between "a lot of something weak" and "a little of something strong"
- Predicts that a small source can heat a thin wire to glow, while a large source can barely warm a thick one
- Lets you design something before you build it, not just observe after the fact

## What Would You Try?

- A muscle twitches, a spark jumps, a wire heats. Imagine each is the same invisible thing in motion. What are the minimum two properties it needs to have?
- You have a battery that can power a dim bulb or a bright one. What do you measure to tell them apart? What's different — the battery? the bulb? both?
- Sketch two identical jars, one connected to a lightning rod, one to a small pile of coins and zinc plates. Both can light a tiny wire momentarily. Are they the same? How would you distinguish them?

## Failed Attempts

### Attempt 1: Treat it as a material substance you weigh

Every effect comes in amounts — more lightning means more destruction, more coins in the pile means a longer spark. So treat it as a material substance: if something flows into the wire, the wire should gain mass. You should be able to collect it in a container and weigh what you've gathered. More substance = more effect.

This predicts: a large container of weak substance and a small container of strong substance should do identical work as long as they weigh the same; a big slow stream and a small fast jet carry the same energy.

Experimentally: two setups with the same "amount" behave completely differently. A massive static charge from rubbing amber can jump a centimeter gap but barely warms a wire; a small voltaic pile produces no visible spark but steadily heats wire to glowing. You can't substitute one for the other. Weight or volume is the wrong measure — or rather, it captures only half the story.

The failure reveals: there are two independent quantities. Something about *how hard it pushes* is separate from something about *how much is flowing*. They can be traded against each other, but you need both.

### Attempt 2: Sparks, shocks, and heat are different substances

Maybe they're different phenomena that just happen to coexist. "Electrical fluid" causes sparks; "galvanic fluid" from metals causes muscle twitches; "caloric" causes the heat. Measure each separately.

This would predict: you could have sparks without heat, or heat without any possibility of a shock. You could store caloric in one container and electrical fluid in another and combine them at will.

Experimentally: wherever you get current flowing, heat always accompanies it — always, in every material. The spark is just a very fast, very concentrated version of the same process. And Volta's pile, which produces no dramatic spark, can still cause a muscle twitch AND heat a wire AND eventually jump a small gap. It's all the same thing, varying in rate and intensity.

The failure reveals: treating three manifestations as three substances wastes the unifying explanation. One thing, measured two ways, accounts for all of them.

### Attempt 3: One number is enough

If there's one substance, one number describes it. Measure the "charge" and you know everything.

This predicts: two sources with the same charge reading should be interchangeable. A large Leyden jar (stores a lot of charge) should do the same work per moment as a voltaic pile (produces continuous push but holds little charge).

Experimentally: the Leyden jar delivers all its energy in a single violent instant and is then dead. The pile delivers steady, controllable energy over hours. They carry equivalent total charge yet behave nothing alike. The *rate* at which charge moves — and the *pressure* behind it — matters as much as the total amount.

The failure reveals: you need the *rate of flow* as a separate quantity, not just the total. And the pressure driving that flow is yet another quantity, independent of how much flows.

## The Discovery

One invisible thing, but two handles to grab it with.

The first handle: how hard is it being pushed? A lightning bolt pushes with millions of volts; a voltaic pile pushes with roughly one volt per pair of metals. This is the *push* — what you'd later call **voltage**. It determines whether a spark can jump a gap, whether a current can flow through a poor conductor, how much energy each unit of flow carries.

The second handle: how much flows per moment? A lightning bolt delivers its charge in microseconds. A pile delivers it steadily over hours. This is the *flow rate* — what you'd later call **current**. It determines how much work happens per second, how hot a wire gets, how strongly a magnet is energized.

Power — the rate of doing work — is both handles together: **P = V × I**. A high voltage pushing a small current can equal a low voltage pushing a large current. But they're not interchangeable in practice: a 1000 V, 1 mA source can light a neon tube but not run a motor; a 1 V, 1 A source can run a motor but not jump any gap.

To measure voltage you need a device that responds to push without drawing much flow — a **voltmeter**. To measure current you need a device that sits inside the path and counts flow — an **ammeter**. Your invisible something now has a name, two handles, and two instruments. You can design before you build.

## Try It

<iframe src="../assets/browser/chapter01/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter01/index.html)

Before changing anything, predict:

- If you double the voltage while keeping resistance constant, what happens to the power?
- Can you find a combination of voltage and current that gives 10 W in two different ways? Do they feel different in the sim?
- If the voltmeter shows 5 V and the ammeter shows 0.5 A, how much energy is delivered in 10 seconds?

## Implementation

The sim presents two sliders — voltage (V) and current (I) — and plots power (P = V × I) in real time alongside a glowing-wire visual whose brightness scales with P. A "source type" toggle switches between a capacitor model (high voltage, decaying current) and a battery model (stable voltage, steady current) to make concrete the failure of "one number is enough."

## When It Breaks

**High voltage, unmeasured.** A voltmeter draws a tiny current to make its reading — if the source can't supply even that, the reading is wrong. Electrostatic sources (rubbed amber, Van de Graaff generators) can't sustain any current draw; their "voltage" reading collapses the moment you try to measure it.

**Power without direction.** P = V × I gives magnitude but not sign. In circuits where current can reverse, power can be delivered or absorbed by the same device. Ignoring sign leads to heat budgets that appear balanced but have sources and loads backwards.

## Transfer

- **Defibrillators**: the device charges a capacitor to ~1000 V (high push) then discharges it in ~10 ms through the chest (~40 A). Both handles matter: too little voltage can't penetrate tissue resistance; too little current can't depolarize enough muscle.
- **USB power delivery**: 5 V × 1 A = 5 W for phones; 20 V × 5 A = 100 W for laptops. Same connector, different voltage-current trade-off — your charger negotiates both handles before delivering power.
- **Power lines**: electricity is transmitted at ~500 kV and tiny current, then stepped down. Same power delivered at lower voltage would require current so large the wire would melt.

Exercises:

1. A 9 V battery powers a motor drawing 300 mA. How much power is delivered? How much energy in 2 minutes?
2. Two sources: Source A is 12 V, 2 A. Source B is 6 V, 4 A. Same power. Describe a circuit where A works but B fails, and another where B works but A fails.
3. A voltmeter reads 5 V across a component. An ammeter in series reads 0 A. What does this tell you about the component? What if the ammeter reads 0.1 A instead?

---

**Continue → [Why It Needs a Path](02-why-it-needs-a-path.md)**
