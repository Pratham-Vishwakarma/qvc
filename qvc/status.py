import json
from .database import get_staged_data

def show_summary_status():
    stage_data = get_staged_data()

    if not stage_data:
        print("No staged data.")
    else:
        rows = []

        for row in stage_data:
            stage_id = row[0][:8]
            timestamp = row[1]

            circuit = json.loads(row[2])
            parameters = json.loads(row[3])
            bindings = json.loads(row[4])
            statevector = json.loads(row[5])

            rows.append({
                "id": stage_id,
                "day": timestamp.split("T")[0],
                "time": timestamp.split("T")[1][:8],
                "gates": len(circuit),
                "params": len(parameters),
                "bindings": len(bindings),
                "state_dim": len(statevector)
            })

        if not rows:
            print("Stage is empty")
            return

        headers = rows[0].keys()

        widths = {
            h: max(len(h), max(len(str(r[h])) for r in rows))
            for h in headers
        }

        print(" | ".join(f"{h:<{widths[h]}}" for h in headers))
        print("-+-".join("-" * widths[h] for h in headers))

        for r in rows:
            print(" | ".join(f"{str(r[h]):<{widths[h]}}" for h in headers))

def show_detailed_status():
    stage_data = get_staged_data()

    if not stage_data:
        print("No staged data.")
    else:
        for row in stage_data:
            gate = []
            stage_id = row[0]
            timestamp = row[1]

            circuit = json.loads(row[2])
            parameters = json.loads(row[3])
            bindings = json.loads(row[4])
            statevector = json.loads(row[5])

            print(f"\n=== Stage: {stage_id[:8]} ===")
            print(f"Time: {timestamp}")

            # Gates
            print("\nGates:")
            for g in circuit:
                gate.append({
                    "gate": g["gate"],
                    "qubits": str(g["qubits"]),
                    "params": str(g["params"])
                })

            headers = gate[0].keys()

            widths = {
                h: max(len(h), max(len(str(gt[h])) for gt in gate))
                for h in headers
            }

            print(" | ".join(f"{h:<{widths[h]}}" for h in headers))
            print("-+-".join("-" * widths[h] for h in headers))

            for gt in gate:
                print(" | ".join(f"{str(gt[h]):<{widths[h]}}" for h in headers))

            print("\nParameters:")
            for k, v in bindings.items():
                print(f"  {k}: {v}")

            print("\nBindings:")
            for k, v in parameters.items():
                v_copy = v.copy()  # avoid mutating original
                if "uuid" in v_copy:
                    v_copy["uuid"] = v_copy["uuid"][:8]

                print(f"  {k}: {v_copy}")

            print("\nStatevector:")
            for s in statevector:
                print(f"  {s}")