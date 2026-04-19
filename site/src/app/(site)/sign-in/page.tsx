import { AuthStatusPanel } from "@/components/auth/auth-status-panel";
import { PageHeading } from "@/components/page-heading";

export default function SignInPage() {
  return (
    <>
      <PageHeading
        description="Sign in before checkout so purchases can be attached to an account library and install code."
        eyebrow="Auth"
        title="Sign in"
      />
      <div className="mx-auto max-w-xl px-6 py-8 sm:px-10 lg:px-14">
        <AuthStatusPanel mode="sign-in" />
      </div>
    </>
  );
}
