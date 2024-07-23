import { Animal, AnimalWithEvents } from "@/utils/types";
import instance from "./axios";
import { AnimalSchema } from "./schemas/animal";

export async function getAnimals() {
  const res = await instance.get("/animals");
  return res.data as Animal[];
}

export async function createAnimal(values: AnimalSchema) {
  const res = await instance.post("/animals", values);
  return res;
}

export async function updateAnimal(values: AnimalSchema, animalId: string) {
  const res = await instance.put(`/animals/${animalId}`, values);
  return res;
}

export async function getAnimal(animalId: string) {
  const res = await instance.get(`/animals/${animalId}`);
  if (res.status !== 200) throw new Error(res.data);
  return res.data as Animal;
}

export async function getAnimalDetails(animalId: string) {
  const res = await instance.get(`/animals/${animalId}/details`);
  if (res.status !== 200) throw new Error(res.data);
  return res.data as AnimalWithEvents;
}

export type AnimalStatus = {
  animal: Animal;
  status: "available" | "unavailable" | "checked_out";
  status_description: string;
};

export async function getAnimalsWithStatus(zoo_id?: string) {
  const res = await instance.get(
    "/animals/status",
    zoo_id
      ? {
          params: { zoo_id },
        }
      : {},
  );
  return res.data as AnimalStatus[];
}

export async function makeAnimalUnavailable(animalId: string) {
  const res = await instance.put(`/animals/${animalId}/unavailable`);
  return res;
}

export async function makeAnimalAvailable(animalId: string) {
  const res = await instance.put(`/animals/${animalId}/available`);
  return res;
}
