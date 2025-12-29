import click

PARETO_TEMPLATE = """
<objective>
Apply Pareto's principle to {context}.

Identify the vital few factors (≈20%) that drive the majority of results (≈80%),
 cutting through noise to focus on what actually matters.
</objective>

<process>
1. Identify all factors, options, tasks, or considerations in scope
2. Estimate relative impact of each factor on the desired outcome
3. Rank by impact (highest to lowest)
4. Identify the cutoff where ~20% of factors account for ~80% of impact
5. Present the vital few with specific, actionable recommendations
6. Note what can be deprioritized or ignored
</process>

<output_format>
**Vital Few (focus here):**
- Factor 1: [why it matters, specific action]
- Factor 2: [why it matters, specific action]
- Factor 3: [why it matters, specific action]

**Trivial Many (deprioritize):**
- Brief list of what can be deferred or ignored

**Bottom Line:**
Single sentence on where to focus effort for maximum results.
</output_format>
"""

@click.group()
def consider():
    """Apply thinking models to your context."""
    pass

@consider.command()
@click.argument('context', required=False, default="current context")
def pareto(context):
    """Apply Pareto's principle (80/20 rule)."""
    click.echo(PARETO_TEMPLATE.format(context=context))
