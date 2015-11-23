Implement a simple search service (complete with suitable test coverage) using a suitable Python web framework
(micro frameworks welcome).
The purpose is to find artists that match an age range (minimum to maximum) where results are
ordered and returned by best fit.

The best fit algorithm is open to your choice,
but should favour artists with ages in the middle of the range over those at the edge of the range.

The output from the search function should be a JSON encoded structure with a list of matching artist UUIDs
and ages