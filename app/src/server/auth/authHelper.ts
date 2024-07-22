import { prisma } from 'wasp/server';
import { randomInt } from 'node:crypto';

export async function generateAvailableUsername(
  userName: string,
  config: Record<string, string>
) {
  const user = await prisma.user.findFirst({
    where: {
      username: userName,
    },
    select: {
      id: true,
    },
  });
  if (!user) {
    console.log('Username is available.');
    return userName;
  } else {
    console.log('Username is not available.');
    const usernameSegments = userName.split(' ');
    const separator = config?.separator || '-';
    const baseUsername = usernameSegments.join(separator);

    const potentialUsernames = [];
    for (let i = 0; i < 10; i++) {
      const potentialUsername = `${baseUsername}${separator}${randomInt(
        100_000
      )}`;
      potentialUsernames.push(potentialUsername);
    }

    return findAvailableUsername(potentialUsernames);
  }
}

// Checks the database for an unused username from an array provided and returns first.
async function findAvailableUsername(potentialUsernames: any) {
  const users = await prisma.user.findMany({
    where: {
      username: { in: potentialUsernames },
    },
  });
  const takenUsernames = users.map((user) => user.username);
  const availableUsernames = potentialUsernames.filter(
    (username: string) => !takenUsernames.includes(username)
  );

  if (availableUsernames.length === 0) {
    throw new Error(
      'Unable to generate a unique username. Please contact Wasp.'
    );
  }

  return availableUsernames[0];
}
