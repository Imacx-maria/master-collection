import { LibraryList } from "@/components/account/library-list";
import { PageHeading } from "@/components/page-heading";
import { getLibraryItems } from "@/lib/account";

export default function AccountLibraryPage() {
  const items = getLibraryItems();

  return (
    <>
      <PageHeading
        description="Purchased templates and components with package status and install-code access."
        eyebrow="Account"
        title="Library"
      />
      <div className="mx-auto max-w-[1400px] px-6 py-8 sm:px-10 lg:px-14">
        <LibraryList items={items} />
      </div>
    </>
  );
}
