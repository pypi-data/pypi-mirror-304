from pyld import jsonld
import json

CACHED_CONTEXTS = {
    "https://www.w3.org/2018/credentials/v1": "vcdm/linked_data/contexts/credentials/v1",
    "https://www.w3.org/ns/credentials/v2": "vcdm/linked_data/contexts/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2": "vcdm/linked_data/contexts/credentials/examples_v2",
}


class LDProcessorError(Exception):
    """Generic LDProcessorError Error."""


class LDProcessor:
    def __init__(self, strict=True, allowed_ctx=[]):
        self.strict = strict
        self.allowed_ctx = allowed_ctx

    def dropped_terms(self):
        pass

    def dropped_types(self):
        pass

    def dropped_attributes(self):
        pass

    def load_cached_ctx(self, context_url):
        if context_url in CACHED_CONTEXTS:
            with open(f"{CACHED_CONTEXTS[context_url]}.jsonld", "r") as f:
                context = json.loads(f.read())
            return context
        elif context_url in self.allowed_ctx:
            # TODO Fetch and cache context
            return context_url
        else:
            if self.strict:
                raise LDProcessorError("Strict mode on, rejecting unknown context.")

    def try_compact(self, context):
        try:
            jsonld.compact({}, context)
            return True
        except Exception:
            raise LDProcessorError("Error compacting context.")

    def is_valid_context(self, context):
        for idx, ctx_entry in enumerate(context):
            if isinstance(ctx_entry, str):
                context[idx] = self.load_cached_ctx(ctx_entry)
            elif isinstance(ctx_entry, dict):
                return False
        return self.try_compact(context)
