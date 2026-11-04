import { GolemNetwork } from "@golem-sdk/golem-js";

const seen = new Set();

const glm = new GolemNetwork({
  network: "polygon",
});

try {
  await glm.connect();

  const scanSpec = glm.market.buildScanSpecification({
    subnetTag: "public",
    payment: {
      network: "polygon",
      driver: "erc20",
    },
  });

  const sub = glm.market.scan(scanSpec).subscribe({
    next: (offer) => {
      const id =
        offer?.provider?.id ||
        offer?.issuerId ||
        offer?.issuer ||
        offer?.providerId;

      if (id && !seen.has(id)) {
        seen.add(id);
        console.log("provider:", id, "total:", seen.size);
      }
    },
    error: (err) => {
      console.error(err);
    },
  });

  console.log("scanning for 300 seconds...");
  await new Promise((r) => setTimeout(r, 300000));

  sub.unsubscribe();

  console.log("RESULT:", seen.size);
  console.log([...seen]);
} finally {
  await glm.disconnect().catch(() => {});
}
